from django.shortcuts import get_object_or_404
from .models import Event

# イベントから大会を取得する
def get_tournament_by_event(event):
  return event.tournament

# 大会から競技の一覧を取得する
def get_events_by_tournament(tournament):
    return Event.objects.filter(tournament=tournament)