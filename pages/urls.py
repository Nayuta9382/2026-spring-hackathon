from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('tournaments/', TemplateView.as_view(template_name='tournament/list.html'), name='tournament_list'),
    path('tournaments/detail', TemplateView.as_view(template_name='tournament/detail.html'), name='tournament_detail'),
    path('tournaments/edit', TemplateView.as_view(template_name='tournament/edit.html'), name='tournament_edit'),
    path('tournaments/rank-point', TemplateView.as_view(template_name='tournament/rank-point.html'), name='tournament_rank_point'),
    path('events/create', TemplateView.as_view(template_name='events/create.html'), name='events_create'),
    path('events/detail', TemplateView.as_view(template_name='events/detail.html'), name='events_detail'),
    path('teams/edit', TemplateView.as_view(template_name='teams/edit.html'), name='teams_edit'),
    path('event-results/edit', TemplateView.as_view(template_name='event-results/edit.html'), name='event_results_edit'),
    path('schedules/edit', TemplateView.as_view(template_name='schedules/edit.html'), name='schedules_edit'),
]