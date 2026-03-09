from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Event
from teams.service import create_team_group, bulk_create_teams, get_team_group_by_category, get_teams_group_by_event, get_teams_by_event, delete_teams_by_group
from django.db import transaction
from django.shortcuts import get_object_or_404
from tournaments.models import Tournament
from event_results.services import create_event_results, get_event_results_by_event
from .forms import CreateForm
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.views import View
import json


# 競技の新規作成処理
class EventCreateView(CreateView):
    model = Event
    template_name = 'events/create.html'
    form_class = CreateForm

    def form_valid(self, form):
        with transaction.atomic():
            # 大会の取得
            tournament = get_object_or_404(Tournament, pk=self.kwargs.get('tournament_pk'))

            # フォームのインスタンスにセット
            form.instance.tournament = tournament

            team_group_id = 0

            # クラス競技でないなら
            if form.instance.category == 0:
                # チームグループを作成
                new_group = create_team_group(tournament, category=form.instance.category)
                team_group_id = new_group.id

                # チーム保存
                team_names = form.cleaned_data.get('teams', [])
                bulk_create_teams(new_group, team_names)

            else:
                # クラスグループ取得
                class_team_group = get_team_group_by_category(tournament, category=1)
                team_group_id = class_team_group.id

            # チームグループidを保存
            form.instance.team_group_id = team_group_id

            # 競技保存
            response = super().form_valid(form)
            event = self.object

            # 参加チーム取得
            teams = get_teams_group_by_event(event)

            # 競技結果テーブル作成
            create_event_results(event=event, teams=teams)

            return response

    def get_success_url(self):
        return reverse_lazy(
            'tournament_detail_admin',
            kwargs={'pk': self.object.tournament.id}
        )


# 競技の詳細(管理者)
class EventAdminDetailView(DetailView):
    model = Event
    template_name = 'events/admin-detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event = self.object

        teams = get_teams_by_event(event)
        context['teams'] = teams

        event_results = get_event_results_by_event(event=event)
        context['event_results'] = event_results

        schedules = event.schedules.all().order_by('order')
        context['now_schedules'] = schedules.filter(status=0)
        context['next_schedules'] = schedules.filter(status=1)
        context['previous_schedules'] = schedules.filter(status=2)
        context['tournament'] = event.tournament

        return context


# 競技の詳細(一般)
class EventUserDetailView(DetailView):
    model = Event
    template_name = 'events/user-detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event = self.get_object()

        # 競技結果
        event_results = get_event_results_by_event(event=event)
        context['event_results'] = event_results

        # スケジュール
        schedules = event.schedules.all().order_by('order')
        context['now_schedules'] = schedules.filter(status=0)
        context['next_schedules'] = schedules.filter(status=1)
        context['previous_schedules'] = schedules.filter(status=2)
        context['tournament'] = event.tournament

        return context


# 競技の編集
class EventEditView(UpdateView):
    model = Event
    template_name = 'events/edit.html'
    context_object_name = 'event'
    form_class = CreateForm

    # templateに渡す値
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        event = self.get_object()

        teams = get_teams_by_event(event)

        if event.category == 1:
            teams = []

        context['teams'] = teams

        return context

    def form_valid(self, form):
        event = form.instance
        tournament = event.tournament
        teams = form.cleaned_data.get('teams')

        with transaction.atomic():

            # クラス競技
            if form.instance.category == 1:
                class_team_group = get_team_group_by_category(tournament, category=1)
                event.team_group = class_team_group

            else:
                # チームグループ作成
                new_group = create_team_group(tournament, category=0)
                event.team_group = new_group

                # チーム保存
                bulk_create_teams(new_group, teams)

            response = super().form_valid(form)

            return response

    def get_success_url(self):
        return reverse_lazy(
            'event_detail_admin',
            kwargs={
                'tournament_pk': self.object.tournament.id,
                'pk': self.object.id
            }
        )


# 競技削除
class EventDeleteView(DeleteView):
    model = Event

    def get_success_url(self):
        return reverse_lazy(
            'tournament_detail_admin',
            kwargs={'pk': self.object.tournament.url_uuid}
        )

# 競技結果表示
class EventResultsAPIView(View):
    def get(self, request, tournament_pk, pk):

        event = get_object_or_404(Event, pk=pk)
        results = get_event_results_by_event(event)

        # pointごとにチームをまとめる
        point_map = {}
        for r in results:
            team_name = r.team.name
            try:
                team_name = json.loads(team_name)["name"]
            except:
                pass

            point = r.point
            rank = r.rank

            if point not in point_map:
                point_map[point] = {"teams": [], "rank": rank, "point": point}
            point_map[point]["teams"].append(team_name)

        data = []
        for point, entry in sorted(point_map.items(), key=lambda x: x[1]["rank"]):
            data.append({
                "teams": "／".join(entry["teams"]),
                "rank": entry["rank"],
                "point": entry["point"],
            })

        return JsonResponse({"results": data}, json_dumps_params={'ensure_ascii': False})
