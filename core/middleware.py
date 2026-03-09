# core/middleware.py
import re
from django.utils.deprecation import MiddlewareMixin
from tournaments.models import Tournament  # あなたのモデルのパスに合わせてください

class TournamentDiscoveryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        URLにUUIDが含まれているかチェックし、あればDBから取得してrequestに保持する
        """
        # 正規表現でURLからUUIDを抽出
        match = re.search(r'/tournaments/([0-9a-f-]+)', request.path)

        # match 除外リスト
        EXCLUDE_LIST = ['add']
        
        if match:
            tournament_uuid = match.group(1)

            # 1. 除外リストに含まれているかチェック
            if tournament_uuid in EXCLUDE_LIST:
                request._current_tournament = None
            else:
                try:
                    # 後でContext Processorが使いやすいように request に格納
                    request._current_tournament = Tournament.objects.get(url_uuid=tournament_uuid)
                except (Tournament.DoesNotExist, ValueError):
                    request._current_tournament = None
        else:
            request._current_tournament = None