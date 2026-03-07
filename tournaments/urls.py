from django.urls import path
from .views import TournamentCreateView, TournamentListView, TournamentDetailSuperuserView,TournamentDetailUserView, TournamentUpdateView,TournamentDetailOperatorView
from .views import UpdateStatusView
from .views import TournamentDeleteView
from accounts.decorators import admin_required



urlpatterns = [
    # 大会一覧
    path('', admin_required(TournamentListView.as_view()), name='tournament_list'),
    # 大会作成
    path('add', TournamentCreateView.as_view(), name='tournament_create'),

    # <int:pk> を <t_url:pk> に書き換え
    # 管理者(スーパユーザ)大会詳細
    path('<t_url:pk>/admin/superuser', TournamentDetailSuperuserView.as_view(), name='tournament_detail_superuser'),
    # 管理者(運営者)大会詳細
    path('<t_url:pk>/admin/operator', TournamentDetailOperatorView.as_view(), name='tournament_detail_operator'),
    # 一般大会詳細
    path('<t_url:pk>/user', TournamentDetailUserView.as_view(), name='tournament_detail_user'),

    # 大会編集
    path('<int:pk>/edit', TournamentUpdateView.as_view(), name='tournament_update'),
    # 大会ステータスのpulldown
    path('<int:pk>/api/update-status/', UpdateStatusView.as_view(), name='api_update_status'),
     # 大会削除
    path('<t_url:pk>/delete', TournamentDeleteView.as_view(), name='tournament_delete'),

]

