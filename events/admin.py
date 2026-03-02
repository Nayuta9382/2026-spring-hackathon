from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # 一覧画面で見たいフィールドを指定
    list_display = ('id', 'name', 'tournament', 'category', 'created_at')
    
    # フィルタ機能（右側にフィルタメニューが出る）
    list_filter = ('tournament', 'category')
    
    # 検索機能（競技名や大会名で検索可能に）
    search_fields = ('name', 'tournament__name')
    
    # リンクとしてクリックできるフィールド
    list_display_links = ('id', 'name')