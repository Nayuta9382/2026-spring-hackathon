from django.db import transaction,connection
from .models import EventResult
from django.shortcuts import get_object_or_404
# teamの一覧から競技結果のレコードを作成する
def create_event_results(event,teams):
    results = [
        EventResult(
            event=event, 
            team=team, 
            rank=0,
            point=0 
        ) 
        for team in teams
    ]
    
    # 一括で一括保存
    return EventResult.objects.bulk_create(results)

# 競技から競技結果の一覧を取得する
def get_event_results_by_event(event):
    return EventResult.objects.filter(event=event).order_by('rank')

# 競技のID(pk)から競技結果の一覧を取得する
def get_event_results_by_event_id(event_id):
    # event_id フィールド（ForeignKey）を直接指定してフィルタリング
    return EventResult.objects.filter(event_id=event_id).order_by('rank')

