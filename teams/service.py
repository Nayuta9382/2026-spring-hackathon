from .models import TeamGroup, Team
from django.db import transaction
from events.models import Event
from django.shortcuts import get_object_or_404
from events.service import get_team_group_id



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

# 競技からチームの一覧を取得する
def get_teams_by_event(event):
    if event.team_group:
        return Team.objects.filter(team_group=event.team_group).order_by('id')
    return Team.objects.none()

# チームグループからチームの一覧を取得する
def get_teams_by_teamGroup(teamGroup):
    return Team.objects.filter(team_group=teamGroup).order_by('id')

# 競技(event)から紐付いているグループを取得する
def get_teams_group_by_event(event):
    if event.team_group:
        return event.team_group.teams.all()
    
    return [] # グループがない場合は空リストを返す


# 競技idからクラスグループオブジェクトを取得する
def get_team_group_by_event(event_id):
    # チームグループidを取得する
    target_group_id = get_team_group_id(event_id=event_id)
    return get_object_or_404(TeamGroup, pk=target_group_id)

    

# チームグループを削除する(チームはCASCADEで削除)
def delete_team_group(tournament,category=1):
    TeamGroup.objects.filter(category=category, tournament=tournament).delete()

# チームグループに紐づいているチームを削除する
def delete_teams_by_group(team_group):
    if team_group:
        return Team.objects.filter(team_group=team_group).delete()
    return None