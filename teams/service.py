from .models import TeamGroup, Team
from django.db import transaction
from events.models import Event
from django.shortcuts import get_object_or_404



# チームグループを作成する
def create_team_group(tournament, category=1):
    return TeamGroup.objects.create(tournament=tournament, category=category)

# チームを一括で作成する
def bulk_create_teams(team_group, team_names):
    if not team_names:
        return []

    teams = [
        Team(team_group=team_group, name=t_name)
        for t_name in team_names
    ]
    # bulk_createで一括保存
    return Team.objects.bulk_create(teams)

# 指定した大会(tournament)かつ、カテゴリーが1のグループを1つ取得する
def get_team_group_by_category(tournament, category=1):
    return TeamGroup.objects.filter(
        tournament=tournament, 
        category=category
    ).first()

# 競技(event)から紐付いているグループを取得する
def get_teams_by_event(event):
    if event.team_group:
        return event.team_group.teams.all()
    
    return [] # グループがない場合は空リストを返す