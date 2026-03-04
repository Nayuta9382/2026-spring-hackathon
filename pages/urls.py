from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('accounts/operator-login', TemplateView.as_view(template_name='accounts/operator-login.html')),
    path('tournaments/', TemplateView.as_view(template_name='tournament/list.html')),
    path('tournaments/admin-detail', TemplateView.as_view(template_name='tournament/admin-detail.html')),
    path('tournaments/user-detail', TemplateView.as_view(template_name='tournament/user-detail.html')),
    path('tournaments/edit', TemplateView.as_view(template_name='tournament/edit.html')),
    path('tournaments/rank-point', TemplateView.as_view(template_name='tournament/rank-point.html')),
    path('events/create', TemplateView.as_view(template_name='events/create.html')),
    path('events/admin-detail', TemplateView.as_view(template_name='events/admin-detail.html')),
    path('events/user-detail', TemplateView.as_view(template_name='events/user-detail.html')),
    path('teams/edit', TemplateView.as_view(template_name='teams/edit.html')),
    path('event-results/edit', TemplateView.as_view(template_name='event-results/edit.html')),
    path('schedules/edit', TemplateView.as_view(template_name='schedules/edit.html')),
]