from schedules.views import ScheduleUpdateView, ScheduleListView
from django.urls import path

urlpatterns = [
  # スケジュール一覧
    path('<int:pk>/', ScheduleListView.as_view(), name='schedule_list'),
    # スケジュール編集
    path('<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_edit'),
 ]