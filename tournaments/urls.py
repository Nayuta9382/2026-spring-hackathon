from django.urls import path
from .views import TournamentCreateView

urlpatterns = [
    # path(URLの文字列, ビュー, 名前)
    path('create/', TournamentCreateView.as_view(), name='create'),
]