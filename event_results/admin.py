from django.contrib import admin
from .models import EventResult

@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    # 一覧画面で見たい項目
    list_display = ('event', 'rank', 'team', 'point', 'created_at')
    
    # フィルタ機能（右側にフィルタが出る）
    list_filter = ('event', 'rank')
    
    # 検索機能
    search_fields = ('team__name', 'event__name')
    
    # 編集画面で順序を整理
    fields = ('event', 'team', 'rank', 'point', 'detail')