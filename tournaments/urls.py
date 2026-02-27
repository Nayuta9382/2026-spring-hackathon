from django.urls import path
from .views import TournamentCreateView, TournamentListView

urlpatterns = [
    # path(URLの文字列, ビュー, 名前)
    path('create/', TournamentCreateView.as_view(), name='create'),
    path('', TournamentListView.as_view(), name='list'),
]