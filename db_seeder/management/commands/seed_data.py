from django.core.management.base import BaseCommand
from django.db import transaction
from tournaments.models import Tournament, TournamentPoint
from teams.models import TeamGroup, Team
from events.models import Event
from event_results.models import EventResult
from schedules.models import Schedule

# ==========================================
# 設定データ
# ==========================================
TOURNAMENTS_DATA = [
    {
        "name": "2025年eスポーツ大会",
        "password": "pass_esports",
        "cat1_teams": ["システム1・2年", "システム3・4年"], # クラスチーム
        "cat0_teams": ["一般チームA", "一般チームB"],      # 一般チーム
        "events": [
            {"name": "マリオカート", "cat": 1}, # クラス対抗競技
            {"name": "スマブラ", "cat": 0},     # 一般競技
        ],
    },
    {
        "name": "2025年スポーツ大会",
        "password": "pass_sports",
        "cat1_teams": ["1年A組", "1年B組", "2年A組", "2年B組"],
        "cat0_teams": [],
        "events": [
            {"name": "バスケットボール", "cat": 1},
            {"name": "バレーボール", "cat": 1},
        ],
    },
]

class Command(BaseCommand):
    help = 'カテゴリー0と1を正しく分離して生成します'

    def handle(self, *args, **options):
        self.stdout.write("データ生成を開始します...")
        default_points = [10, 8, 6, 4, 2, 1]

        with transaction.atomic():
            Tournament.objects.all().delete()

            for info in TOURNAMENTS_DATA:
                # 1. 大会作成
                tournament = Tournament.objects.create(
                    name=info["name"],
                    password=info["password"]
                )

                # 2. 大会ポイント作成 (cat1のチーム数分)
                cat1_count = len(info["cat1_teams"])
                for i in range(1, cat1_count + 1):
                    p_value = default_points[i-1] if i <= len(default_points) else 0
                    TournamentPoint.objects.create(tournament=tournament, rank=i, point=p_value)

                # --- 3. チームグループ & チームの作成 ---
                groups = {}

                # 【カテゴリー1】の作成
                tg1 = TeamGroup.objects.create(tournament=tournament, category=1)
                groups[1] = tg1
                for t_name in info["cat1_teams"]:
                    Team.objects.create(team_group=tg1, name=t_name)

                # 【カテゴリー0】の作成 (データがある場合のみ)
                if info["cat0_teams"]:
                    tg0 = TeamGroup.objects.create(tournament=tournament, category=0)
                    groups[0] = tg0
                    for t_name in info["cat0_teams"]:
                        Team.objects.create(team_group=tg0, name=t_name)

                # --- 4. 競技(Event)作成 ---
                for e_info in info["events"]:
                    target_cat = e_info["cat"]
                    target_group = groups.get(target_cat)

                    # 該当カテゴリーのグループが存在しない場合はスキップ
                    if not target_group:
                        continue

                    event = Event.objects.create(
                        tournament=tournament,
                        team_group=target_group, # 0か1、正しいグループを紐付け
                        name=e_info["name"],
                        category=target_cat
                    )

                    # 5. スケジュール作成
                    Schedule.objects.create(event=event, detail="本番", order=1)

                    # 6. 競技結果(EventResult)作成
                    # その競技のカテゴリーに属するチームから結果を出す
                    teams_in_group = Team.objects.filter(team_group=target_group)
                    if teams_in_group.count() >= 2:
                        EventResult.objects.create(event=event, team=teams_in_group[0], rank=1, point=10)
                        EventResult.objects.create(event=event, team=teams_in_group[1], rank=2, point=8)

                self.stdout.write(f" - {info['name']}: カテゴリー0と1を分けて生成しました")

        self.stdout.write(self.style.SUCCESS("すべてのデータの生成が完了しました！"))