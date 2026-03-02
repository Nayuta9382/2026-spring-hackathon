from django.db import transaction,connection
from .models import Tournament, TournamentPoint
from teams.models import TeamGroup, Team
from django.shortcuts import get_object_or_404

# 大会作成機能のサービス関数
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

# 大会idから詳細情報を取得する
def get_tournament_detail(id):
    tournament = get_object_or_404(Tournament, pk=id)

    return tournament


# 大会idからその大会のクラスの総合順位を取得する
def get_tournament_rannkings(tournament_id):
    query = """
        SELECT 
            t.name AS name,
            SUM(er.point) AS total_point,
            RANK() OVER (ORDER BY SUM(er.point) DESC) AS rank
        FROM teams_teamgroup tg
        INNER JOIN teams_team t 
            ON tg.id = t.team_group_id
        INNER JOIN events_event e 
            ON tg.id = e.team_group_id
        INNER JOIN event_results_eventresult er 
            ON e.id = er.event_id
        WHERE 
            tg.tournament_id = %s
        GROUP BY 
            t.id, t.name
        ORDER BY 
            rank;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [tournament_id])
        
        # 全行取得して辞書のリストにする
        columns = [col[0] for col in cursor.description]
        rankings = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return rankings