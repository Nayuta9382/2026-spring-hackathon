from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import DetailView,UpdateView
from django.urls import reverse_lazy
from .models import Event
from teams.service import create_team_group,bulk_create_teams,get_team_group_by_category,get_teams_group_by_event,get_teams_by_event,delete_teams_by_group
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
                teams = get_teams_group_by_event(event)

                # 競技結果のテーブルの作成
                create_event_results(event=event,teams=teams)

                return response

    def get_success_url(self):
        # 保存成功後の遷移先（大会詳細ページなど）
        return reverse_lazy('tournament_detail_admin', kwargs={'pk': self.object.tournament.id})

# 競技の詳細(管理者)
class EventAdminDetailView(DetailView):
    model = Event
    template_name = 'events/admin-detail.html'
    context_object_name = 'event'

# 競技の編集
class EventEditView(UpdateView):
    model = Event
    template_name = 'events/edit.html'
    context_object_name = 'event'
    form_class = CreateForm

     # templateファイルに渡す値を取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 登録されているクラスチームの一覧を取得する
        event = self.get_object()
        teams = get_teams_by_event(event)
        if event.category == 1:
            teams = []
        # contextに保存
        context['teams'] = teams

        return context
    
    def form_valid(self, form):
        
        # 2. データの取り出し
        event = form.instance
        tournament = event.tournament
        teams = form.cleaned_data.get('teams')
        with transaction.atomic():
            # クラス競技かどうか
            if form.instance.category == 1:
                # クラスグループを利用
                class_team_group = get_team_group_by_category(tournament, category=1)
                event.team_group = class_team_group
            else:
                # ガチチームを作成する
                # 既存のチームの削除等は時間があれば
                # チームグループを作成する
                new_group = create_team_group(tournament,category = 0)
                event.team_group = new_group
                # # チームを保存する
                bulk_create_teams(new_group, teams)


            # 競技を保存する
            response = super().form_valid(form)

            return response
    
    def get_success_url(self):
        # self.object は Event インスタンス
        return reverse_lazy('event_edit', kwargs={
            'tournament_pk': self.object.tournament.id, # 親のトーナメントID
            'pk': self.object.id                        # このイベント自身のID
        })