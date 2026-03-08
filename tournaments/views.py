from django.views.generic import CreateView, UpdateView,ListView,DetailView
from .models import Tournament,TournamentPoint
from .forms import CreateForm
from .services import create_tournament_with_teams, get_tournament_rannkings,update_tournament_after
from teams.service import get_team_group_by_category,get_teams_by_teamGroup
from events.service import get_events_by_tournament
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import UpdateStatusForm
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from rest_framework import status




# 大会を一覧表示する
class TournamentListView(ListView):
    template_name = 'tournament/list.html'
    model = Tournament

# 大会を作成する
class TournamentCreateView(CreateView):
    model = Tournament
    form_class = CreateForm
    template_name = "tournament/create.html"
    def form_valid(self, form):
        # Serviceを呼び出しデータベースへ保存
        new_tournament =  create_tournament_with_teams(form.cleaned_data)
        self.object = new_tournament

        return redirect(self.get_success_url())

    # 大会詳細にリダイレクト
    def get_success_url(self):
        return reverse('tournament_detail_admin', kwargs={'pk': self.object.pk})

# スーパユーザの大会詳細情報を取得する
class TournamentDetailSuperuserView(DetailView):
    model = Tournament
    template_name = 'tournament/superuser-detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        # 1. まず親クラスの標準的なコンテキスト（tournament等）を取得
        context = super().get_context_data(**kwargs)
        tournament = self.object

        # 2. URLからpkを取得（self.object でも取得可能です）
        pk = self.kwargs.get('pk')

        # 3. 追加のランキング情報を取得して、context辞書に入れる
        # これでテンプレート側で {{ rankings }} が使えるようになります
        context['rankings'] = get_tournament_rannkings(pk)

        context['status_form'] = UpdateStatusForm(instance=tournament)

        # クラスチームの一覧を取得する
        team_group = get_team_group_by_category(tournament=self.object,category=1)
        teams = get_teams_by_teamGroup(team_group)
        context['teams'] = teams

        # 競技の一覧を取得する
        events = get_events_by_tournament(tournament=tournament)
        context['events'] = events

        # アプリのホストを取得し、大会URLを作成
        host = settings.APP_HOST
        port = settings.APP_PORT
        protocol = settings.APP_PROTOCOL
        admin_url = f'{protocol}://{host}:{port}/tournaments/{tournament.url_uuid}/admin/operator'
        user_url = f'{protocol}://{host}:{port}/tournaments/{tournament.url_uuid}/user'
        context['admin_url'] = admin_url
        context['user_url'] = user_url


        return context
# 運営者の大会詳細情報を取得する(時間あればスーパユーザと関数統一する)
class TournamentDetailOperatorView(DetailView):
    model = Tournament
    template_name = 'tournament/operator-detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        # 1. まず親クラスの標準的なコンテキスト（tournament等）を取得
        context = super().get_context_data(**kwargs)
        tournament = self.object

        # 2. URLからpkを取得（self.object でも取得可能です）
        pk = self.kwargs.get('pk')

        # 3. 追加のランキング情報を取得して、context辞書に入れる
        # これでテンプレート側で {{ rankings }} が使えるようになります
        context['rankings'] = get_tournament_rannkings(pk)

        context['status_form'] = UpdateStatusForm(instance=tournament)

        # クラスチームの一覧を取得する
        team_group = get_team_group_by_category(tournament=self.object,category=1)
        teams = get_teams_by_teamGroup(team_group)
        context['teams'] = teams

        # 競技の一覧を取得する
        events = get_events_by_tournament(tournament=tournament)
        context['events'] = events

        # アプリのホストを取得し、大会URLを作成
        host = settings.APP_HOST
        port = settings.APP_PORT
        protocol = settings.APP_PROTOCOL
        admin_url = f'{protocol}://{host}:{port}/tournaments/{tournament.url_uuid}/admin/operator'
        user_url = f'{protocol}://{host}:{port}/tournaments/{tournament.url_uuid}/user'
        context['admin_url'] = admin_url
        context['user_url'] = user_url


        return context
    
# 大会詳細(一般)
class TournamentDetailUserView(DetailView):
    model = Tournament
    template_name = 'tournament/user-detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        # 1. まず親クラスの標準的なコンテキスト（tournament等）を取得
        context = super().get_context_data(**kwargs)
        tournament = self.object

        # 2. URLからpkを取得（self.object でも取得可能です）
        pk = self.kwargs.get('pk')

        # 3. 追加のランキング情報を取得して、context辞書に入れる
        # これでテンプレート側で {{ rankings }} が使えるようになります
        context['rankings'] = get_tournament_rannkings(pk)

        context['status_form'] = UpdateStatusForm(instance=tournament)

        # 競技の一覧を取得する
        events = get_events_by_tournament(tournament=tournament)
        context['events'] = events

        return context


# 大会を編集する
class TournamentUpdateView(UpdateView):
    model = Tournament
    form_class = CreateForm # 作成用と同じフォームが使えます
    template_name = "tournament/edit.html" # 編集用のHTML

    # templateファイルに渡す値を取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 登録されているクラスチームの一覧を取得する

        # チームグループの取得
        team_group =  get_team_group_by_category(tournament = self.object,category=1)
        # チームの取得
        teams = get_teams_by_teamGroup(team_group)

        # 基本順位ポイントの取得
        tournament_points = TournamentPoint.objects.filter(tournament = self.object).order_by('rank')

        # contextに保存
        context['teams'] = teams
        context['rank_points'] = tournament_points

        return context

    def form_valid(self, form):
        with transaction.atomic():
            # 2. メインの Tournament を保存（self.object が更新される）
            response = super().form_valid(form)
            tournament = self.object

            teams = form.cleaned_data['team_names']
            rank_points = form.cleaned_data['points']

            # チームと基本順位ポイントを更新する
            update_tournament_after(tournament = tournament,teams = teams, rank_points = rank_points)


        return redirect(self.get_success_url())


    def get_success_url(self):
        # 編集が終わったら、また詳細画面に戻る
        return reverse('tournament_detail_superuser', kwargs={'pk': self.object.pk})

    # 大会ステータスのpulldown
class UpdateStatusView(View):
    def post(self, request, pk):
        try:
            new_status = request.POST.get('status')

            # 対象の大会を取得
            tournament = get_object_or_404(Tournament, pk=pk)

            # ステータスを更新して保存
            if new_status is not None:
                tournament.status = int(new_status)
                tournament.save()

            return redirect('tournament_detail_superuser', pk=pk)

        except Exception as e:
            return redirect('tournament_detail_superuser', pk=pk)

     # 大会を削除する
class TournamentDeleteView(DeleteView):
    model = Tournament
    template_name = 'tournament/delete.html'
    #削除後は大会一覧へリダイレクト
    success_url = reverse_lazy('tournament_list')


# 大会の総合順位を返すapi
class GetTournamentRankAPIView(APIView):
    # GETリクエストの処理
    def get(self, request,pk, format=None):
        pk = self.kwargs.get('pk')

        # ランキングを取得
        data = get_tournament_rannkings(pk)

        # ランキングをjsonに変換
        rankings = defaultdict(list)

        for item in data:
            rank = item['rank']
            rankings[rank].append({
                "name": item['name'],
                "total_point": item['total_point']
            })
        return Response(rankings, status=status.HTTP_200_OK)