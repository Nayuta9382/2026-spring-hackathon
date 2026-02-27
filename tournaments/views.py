from django.views.generic import CreateView, UpdateView,ListView
from .models import Tournament
from .forms import CreateForm
from .services import create_tournament_with_teams
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

