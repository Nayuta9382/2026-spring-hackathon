from schedules.views import ScheduleUpdateView, ScheduleListView
from django.urls import path
from accounts.decorators import admin_required


urlpatterns = [
  # スケジュール一覧
    path('<int:pk>/', admin_required(ScheduleListView.as_view()), name='schedule_list'),
    # スケジュール編集
    path('<int:pk>/edit/', admin_required(ScheduleUpdateView.as_view()), name='schedule_edit'),
 ]