from django.db import transaction
from .models import Tournament, TournamentPoint
from teams.models import TeamGroup, Team

# 大会作成機能のサービスクラス
def create_tournament_with_teams(tournament_data):
    with transaction.atomic():

        
        # 1. 大会作成
        tournament = Tournament.objects.create(
           name=tournament_data.get('name'), 
            password=tournament_data.get('password'), 
            img_path=tournament_data.get('img_path'),         
            pdf_img_path=tournament_data.get('pdf_img_path')
        )

        # 2. チームグループ作成
        team_group = TeamGroup.objects.create(tournament=tournament, category=1)

        # 3. チーム一括作成
        Team.objects.bulk_create([
            Team(team_group=team_group, name=t_name)
            for t_name in tournament_data.get('team_names', [])
        ])

        # 4. ポイント一括作成
        TournamentPoint.objects.bulk_create([
            TournamentPoint(tournament=tournament, rank=i, point=p)
            for i, p in enumerate(tournament_data.get('points', []), 1)
        ])
    
    return tournament