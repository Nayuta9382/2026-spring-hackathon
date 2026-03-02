from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Event
from teams.service import create_team_group,bulk_create_teams,get_team_group_by_category,get_teams_by_event
from django.db import transaction
from django.shortcuts import get_object_or_404
from tournaments.models import Tournament
from event_results.services import create_event_results
from .forms import CreateForm


# Create your views here.


# 競技の新規作成処理
class EventCreateView(CreateView):
    model = Event
    template_name = 'events/create.html'
    form_class = CreateForm
    
    def form_valid(self, form):
            with transaction.atomic():
                # 大会の取得
                tournament = get_object_or_404(Tournament, pk=self.kwargs.get('tournament_pk'))
                # フォームのインスタンスにセット（オブジェクトをそのまま渡せる）
                form.instance.tournament = tournament

                team_group_id = 0
                # クラス競技でないなら
                if(form.instance.category == 0):
                    # チームグループを作成する
                    new_group = create_team_group(tournament,category = form.instance.category)
                    team_group_id = new_group.id

                    # チームを保存する
                    team_names = form.cleaned_data.get('teams', [])
                    bulk_create_teams(new_group, team_names)
                else:
                    # クラスグループidを取得する
                    class_team_group = get_team_group_by_category(tournament, category=1)
                    team_group_id = class_team_group.id

                # チームグループidを競技に保存する
                form.instance.team_group_id = team_group_id

                # 競技を保存する
                response = super().form_valid(form)
                event = self.object
                
                # 競技に参加するチームの一覧を取得する
                teams = get_teams_by_event(event)

                # 競技結果のテーブルの作成
                create_event_results(event=event,teams=teams)

                return response

    def get_success_url(self):
        # 保存成功後の遷移先（大会詳細ページなど）
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.tournament.id})
