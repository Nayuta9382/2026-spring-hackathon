from django.shortcuts import get_object_or_404
from .models import Event
from schedules.models import Schedule
from django.db.models import Prefetch

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

# 競技を再登録する
def register_cloned_event(event_instance, new_team_group_id=None):
    # 主キーを無効化する
    event_instance.pk = None
    event_instance.id = None 

    # チームグループidを置き換える
    event_instance.team_group_id = new_team_group_id

    # 保存
    event_instance.save()

    return event_instance
#指定されたチームグループIDに紐づく全ての競技と、
#その競技に紐づくスケジュール一覧を取得する。
def get_events_with_schedules_by_team_group(team_group_id):

    # スケジュールを order 順に並べ替えて取得するための Prefetch オブジェクト
    schedule_prefetch = Prefetch(
        'schedules',
        queryset=Schedule.objects.all().order_by('order'),
        to_attr='prefetched_schedules' # テンプレート等でアクセスしやすい名前を付ける
    )

    # 1. チームグループIDでフィルタ
    # 2. prefetch_related でスケジュールを一括取得
    events = Event.objects.filter(
        team_group_id=team_group_id
    ).prefetch_related(schedule_prefetch)

    return events