from django.views.generic import CreateView, UpdateView,ListView,DetailView
from .models import Tournament
from .forms import CreateForm
from .services import create_tournament_with_teams, get_tournament_rannkings,get_tournament_detail
from django.shortcuts import redirect



# 大会を一覧表示する
class TournamentListView(ListView):
    template_name = 'tournament/list.html'
    model = Tournament

# 大会を作成する
class TournamentCreateView(CreateView):
    model = Tournament
    form_class = CreateForm
    template_name = "tournament/create.html"
    success_url = "/"  # 成功時にリダイレクトするURL

    def form_valid(self, form):
        data = form.cleaned_data
        
        # Serviceを呼び出しデータベースへ保存
        create_tournament_with_teams(form.cleaned_data)
        
        return redirect(self.success_url)

# 管理者の大会詳細情報を取得する
class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournament/admin-detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        # 1. まず親クラスの標準的なコンテキスト（tournament等）を取得
        context = super().get_context_data(**kwargs)
        
        # 2. URLからpkを取得（self.object でも取得可能です）
        pk = self.kwargs.get('pk')

        # 3. 追加のランキング情報を取得して、context辞書に入れる
        # これでテンプレート側で {{ rankings }} が使えるようになります
        context['rankings'] = get_tournament_rannkings(pk)

        return context

