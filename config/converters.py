# config/converters.py
# 大会のpkとurlを変換する
class TournamentURLConverter:
    regex = '[a-zA-Z0-9_-]+'

    def to_python(self, value):
        from tournaments.models import Tournament
        from django.shortcuts import get_object_or_404
        # 'url' ではなく 'url_uuid' で検索するように修正
        tournament = get_object_or_404(Tournament, url_uuid=value)
        return tournament.pk

    def to_url(self, value):
        from tournaments.models import Tournament
        
        # モデルオブジェクトが渡された場合
        if hasattr(value, 'url_uuid'):
            return str(value.url_uuid)
            
        # ID（数値）で渡された場合
        try:
            tournament = Tournament.objects.get(pk=value)
            return str(tournament.url_uuid)
        except (Tournament.DoesNotExist, ValueError):
            return str(value)