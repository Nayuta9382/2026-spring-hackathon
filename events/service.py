from django.shortcuts import get_object_or_404
from .models import Event

# イベントから大会を取得する
def get_tournament_by_event(event):
  return event.tournament

# イベントidからイベントオブジェクトを取得する
def get_event_by_id(event_id):
    return get_object_or_404(Event, pk=event_id)

# 大会から競技の一覧を取得する
def get_events_by_tournament(tournament):
    return Event.objects.filter(tournament=tournament)


# イベントidからチームグループidを取得する
def get_team_group_id(event_id):
        event = get_object_or_404(Event, id=event_id)
        return event.team_group_id