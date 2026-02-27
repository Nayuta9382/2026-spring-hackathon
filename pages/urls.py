from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('tournaments/', TemplateView.as_view(template_name='tournament/list.html'), name='tournament_list'),
    path('tournaments/admin-detail', TemplateView.as_view(template_name='tournament/admin-detail.html'), name='tournament_admin_detail'),
    path('tournaments/user-detail', TemplateView.as_view(template_name='tournament/user-detail.html'), name='tournament_user_detail'),
    path('tournaments/edit', TemplateView.as_view(template_name='tournament/edit.html'), name='tournament_edit'),
    path('tournaments/rank-point', TemplateView.as_view(template_name='tournament/rank-point.html'), name='tournament_rank_point'),
    path('events/create', TemplateView.as_view(template_name='events/create.html'), name='events_create'),
    path('events/admin-detail', TemplateView.as_view(template_name='events/admin-detail.html'), name='events_admin_detail'),
    path('events/user-detail', TemplateView.as_view(template_name='events/user-detail.html'), name='events_user_detail'),
    path('teams/edit', TemplateView.as_view(template_name='teams/edit.html'), name='teams_edit'),
    path('event-results/edit', TemplateView.as_view(template_name='event-results/edit.html'), name='event_results_edit'),
    path('schedules/edit', TemplateView.as_view(template_name='schedules/edit.html'), name='schedules_edit'),
]