from django.contrib import admin
from .models import EventResult

@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    # 一覧画面に 'is_class_point' を追加
    # BooleanFieldなので、管理画面上では ✅ や ❌ のアイコンで表示されます
    list_display = ('event', 'rank', 'team', 'point', 'created_at')
    
    # フィルタ機能に 'is_class_point' を追加
    # 「対象のみ」を絞り込めるようになるので便利です
    list_filter = ('event', 'rank', )
    
    # 検索機能
    search_fields = ('team__name', 'event__name')
    
    # 編集画面の項目に 'is_class_point' を追加
    fields = ('event', 'team', 'rank', 'point', 'detail')