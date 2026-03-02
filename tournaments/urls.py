from django.urls import path
from .views import TournamentCreateView, TournamentListView,TournamentDetailView
from .views import UpdateStatusView

urlpatterns = [
    # path(URLの文字列, ビュー, 名前)
    path('create', TournamentCreateView.as_view(), name='tournament_create'),
    # 大会一覧
    path('', TournamentListView.as_view(), name='tournament_list'),
    # 管理者大会詳細
    path('<int:pk>/admin', TournamentDetailView.as_view(), name='tournament_detail'),
    # 大会ステータスのpulldwon
    path('<int:pk>/api/update-status/', UpdateStatusView.as_view(), name='api_update_status'),
]