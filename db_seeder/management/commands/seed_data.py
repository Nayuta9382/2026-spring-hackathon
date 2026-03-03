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
        "cat1_teams": ["システム1・2年", "システム3・4年"], # 2チーム → ポイントは2位まで
        "cat0_teams": ["一般チームA-1", "一般チームA-2", "一般チームB-1", "一般チームB-2"],
        "event_names": ["マリオカート", "スマブラ"],
        "use_cat0": True,
    },
    {
        "name": "2025年スポーツ大会",
        "password": "pass_sports",
        "cat1_teams": ["システム1年", "システム2年", "システム3年", "システム4年"], # 4チーム → ポイントは4位まで
        "cat0_teams": [],
        "event_names": ["バスケットボール", "バレーボール"],
        "use_cat0": False,
    },
]

class Command(BaseCommand):
    help = 'カテゴリー1のチーム数に合わせて順位ポイントを生成します'

    def handle(self, *args, **options):
        self.stdout.write("データ生成を開始します...")
        
        # 仮のポイント配分用（1位から順に何点あげるか。チーム数が多い場合に備えて多めに定義）
        default_points = [10, 8, 6, 4, 2, 1, 0, 0, 0, 0]

        with transaction.atomic():
            Tournament.objects.all().delete()

            for info in TOURNAMENTS_DATA:
                # 1. 大会作成
                tournament = Tournament.objects.create(
                    name=info["name"],
                    password=info["password"]
                )

                # 2. 大会ポイント作成 (カテゴリー1のチーム数分だけ作成)
                cat1_count = len(info["cat1_teams"])
                
                point_list = []
                for i in range(1, cat1_count + 1):
                    # default_pointsから取得（足りなければ0点）
                    p_value = default_points[i-1] if i <= len(default_points) else 0
                    point_list.append(
                        TournamentPoint(tournament=tournament, rank=i, point=p_value)
                    )
                
                TournamentPoint.objects.bulk_create(point_list)
                self.stdout.write(f" - {info['name']}: {cat1_count}位までのポイントを作成しました")

                # 3. グループ構成の動的作成
                group_configs = []
                if info.get("use_cat0"):
                    group_configs.append({"cat": 0, "teams": info["cat0_teams"][:2]})
                    group_configs.append({"cat": 0, "teams": info["cat0_teams"][2:4]})
                
                group_configs.append({"cat": 1, "teams": info["cat1_teams"]})

                for config in group_configs:
                    cat = config["cat"]
                    tg = TeamGroup.objects.create(tournament=tournament, category=cat)

                    # 4. チーム作成
                    created_teams = [
                        Team.objects.create(team_group=tg, name=t_name)
                        for t_name in config["teams"]
                    ]

                    # 5. 競技(Event)作成
                    for e_name in info["event_names"]:
                        event = Event.objects.create(
                            tournament=tournament,
                            team_group=tg,
                            name=f"{e_name}(カテゴリー{cat})",
                            category=cat
                        )

                        # 6. スケジュール作成
                        Schedule.objects.create(event=event, detail="本番", order=1)

                        # 7. 競技結果(EventResult)作成
                        if len(created_teams) >= 2:
                            EventResult.objects.create(event=event, team=created_teams[0], rank=1, point=10)
                            EventResult.objects.create(event=event, team=created_teams[1], rank=2, point=5)

        self.stdout.write(self.style.SUCCESS("すべてのデータの生成が完了しました！"))