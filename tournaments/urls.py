from django.urls import path
from .views import TournamentCreateView, TournamentListView, TournamentDetailSuperuserView,TournamentDetailUserView, TournamentUpdateView,TournamentDetailOperatorView,GetTournamentRankAPIView
from .views import UpdateStatusView
from .views import TournamentDeleteView
from accounts.decorators import admin_required,super_user_required,operator_required



urlpatterns = [
    # 大会一覧
    path('', super_user_required(TournamentListView.as_view()), name='tournament_list'),
    # 大会作成
    path('add', super_user_required(TournamentCreateView.as_view()), name='tournament_create'),

    # 管理者(スーパユーザ)大会詳細
    path('<t_url:pk>/admin/superuser', super_user_required(TournamentDetailSuperuserView.as_view()), name='tournament_detail_superuser'),
    # 管理者(運営者)大会詳細
    path('<t_url:pk>/admin/operator', operator_required(TournamentDetailOperatorView.as_view()), name='tournament_detail_operator'),
    # 一般大会詳細
    path('<t_url:pk>/user', TournamentDetailUserView.as_view(), name='tournament_detail_user'),

    # 大会編集
    path('<t_url:pk>/edit', super_user_required(TournamentUpdateView.as_view()), name='tournament_update'),
    # 大会ステータスのpulldown
    path('<int:pk>/api/update-status/', super_user_required(UpdateStatusView.as_view()), name='api_update_status'),
     # 大会削除
    path('<t_url:pk>/delete', super_user_required(TournamentDeleteView.as_view()), name='tournament_delete'),
    # 大会順位を取得する
    path('<t_url:pk>/api/tournament-rank', GetTournamentRankAPIView.as_view(), name='api_tournament_rank_get'),
]

