from django.db import transaction,connection
from .models import EventResult
from django.shortcuts import get_object_or_404
# teamの一覧から競技結果のレコードを作成する
def create_event_results(event,teams):
    results = [
        EventResult(
            event=event, 
            team=team, 
            rank=0  
        ) 
        for team in teams
    ]
    
    # 一括で一括保存
    return EventResult.objects.bulk_create(results)