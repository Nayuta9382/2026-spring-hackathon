from django.contrib import admin
from .models import Tournament, TournamentPoint

# ポイント設定を大会の編集画面で一緒に表示するための設定
class TournamentPointInline(admin.TabularInline):
    model = TournamentPoint
    extra = 0  # デフォルトで表示する空の入力欄の数

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    # 一覧画面で表示する項目
    list_display = ('name', 'status', 'created_at', 'url_uuid')
    
    # 検索ボックスの対象項目
    search_fields = ('name', 'url_uuid')
    
    # フィルタ（絞り込み）機能
    list_filter = ('status', 'created_at')
    
    # 詳細画面にポイント設定を埋め込む
    inlines = [TournamentPointInline]

    # url_uuidなどは編集不可（読み取り専用）にする
    readonly_fields = ('url_uuid', 'created_at')

# ポイント単体でも管理したい場合は登録（不要なら消してOK）
@admin.register(TournamentPoint)
class TournamentPointAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'rank', 'point')
    list_filter = ('tournament',)