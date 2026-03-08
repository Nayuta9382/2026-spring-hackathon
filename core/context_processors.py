# core/context_processors.py

def tournament_context(request):
    # ミドルウェアがセットした値をテンプレート変数 'tournament' として公開
    return {
        'tournament': getattr(request, '_current_tournament', None)
    }