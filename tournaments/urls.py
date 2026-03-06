from django.urls import path
from .views import TournamentCreateView, TournamentListView, TournamentDetailAdminView,TournamentDetailUserView, TournamentUpdateView
from .views import UpdateStatusView
from .views import TournamentDeleteView
from schedules.views import ScheduleUpdateView, ScheduleListView


urlpatterns = [
    # 大会一覧
    path('', TournamentListView.as_view(), name='tournament_list'),
    # 大会作成
    path('add', TournamentCreateView.as_view(), name='tournament_create'),

    # <int:pk> を <t_url:pk> に書き換え
    # 管理者大会詳細
    path('<t_url:pk>/admin', TournamentDetailAdminView.as_view(), name='tournament_detail_admin'),
    # 一般大会詳細
    path('<t_url:pk>/user', TournamentDetailUserView.as_view(), name='tournament_detail_user'),

    # 大会編集
    path('<int:pk>/edit', TournamentUpdateView.as_view(), name='tournament_update'),
    # 大会ステータスのpulldown
    path('<int:pk>/api/update-status/', UpdateStatusView.as_view(), name='api_update_status'),
     # 大会削除
    path('<t_url:pk>/delete', TournamentDeleteView.as_view(), name='tournament_delete'),
    # スケジュール一覧（next/now/previous表示）
    path('schedules/<int:pk>/', ScheduleListView.as_view(), name='schedule_list'),
    # スケジュール編集
    path('schedules/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_edit'),

]

