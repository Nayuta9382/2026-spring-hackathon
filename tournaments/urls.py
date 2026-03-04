from django.urls import path
from .views import TournamentCreateView, TournamentListView,TournamentDetailView,TournamentUpdateView
from .views import UpdateStatusView
from .views import TournamentDeleteView

urlpatterns = [
    # 大会一覧
    path('', TournamentListView.as_view(), name='tournament_list'),
    # 大会作成
    path('add', TournamentCreateView.as_view(), name='tournament_create'),
    # 管理者大会詳細
    path('<int:pk>/admin', TournamentDetailView.as_view(), name='tournament_detail_admin'),
    # 管理者大会編集
    path('<int:pk>/update', TournamentUpdateView.as_view(), name='tournament_update'),
    # 大会ステータスのpulldwon
    path('<int:pk>/api/update-status/', UpdateStatusView.as_view(), name='api_update_status'),
    # 大会削除
    path('<int:pk>/delete', TournamentDeleteView.as_view(), name='tournament_delete'),
]
