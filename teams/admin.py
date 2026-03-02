from django.contrib import admin
from .models import TeamGroup, Team

# チームをグループの編集画面で一緒に表示するための設定
class TeamInline(admin.TabularInline):
    model = Team
    extra = 1  # 最初から表示しておく入力欄の数

@admin.register(TeamGroup)
class TeamGroupAdmin(admin.ModelAdmin):
    # 一覧画面の表示
    list_display = ('id', 'tournament', 'category', 'created_at')
    # フィルタ
    list_filter = ('tournament', 'category')
    # インライン設定（これでグループ詳細画面からチームをいじれる）
    inlines = [TeamInline]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # 'group_id' というカスタム項目を追加
    list_display = ('name', 'group_id', 'team_group', 'created_at')
    search_fields = ('name',)
    list_filter = ('team_group__tournament',)

    # チームグループのIDを返すメソッド
    def group_id(self, obj):
        return obj.team_group.id
    
    # 管理画面上の列見出しを「グループID」に変更
    group_id.short_description = 'グループID'