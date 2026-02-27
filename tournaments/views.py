from django.views.generic import CreateView, UpdateView
from .models import Tournament
from .forms import CreateForm
from .services import create_tournament_with_teams
from django.shortcuts import redirect


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



    # def form_valid(self, form):
    #     teams = [t.strip() for t in self.request.POST.getlist('teams') if t.strip()]
    #     points = [p.strip() for p in self.request.POST.getlist('rank_points') if p.strip()]# 1位から順番に受け取る


    #     # バリデーションを行う
    #     # チームが1つも入力されていない場合
    #     if not teams:
    #         form.add_error(None, "チーム名を1つ以上入力してください。")
    #         return self.form_invalid(form)

    #     # チーム数とポイント数が一致しているか
    #     if len(teams) != len(points):
    #         form.add_error(None, f"チーム数({len(teams)})とポイント設定数({len(points)})が一致しません。")
    #         return self.form_invalid(form)

    #     # ポイントがすべて数値（整数）になっているか
    #     try:
    #         # すべて整数に変換を試みる
    #         points = [int(p) for p in points]
    #     except ValueError:
    #         form.add_error(None, "ポイントには半角数字を入力してください。")
    #         return self.form_invalid(form)


    #     # トランザクション
    #     with transaction.atomic():
    #         # 受け取った画像を保存する


    #         # --- model(大会)への保存処理 ---
    #         response = super().form_valid(form) 
    #         # pk を受け取る
    #         tournament_id = self.object.pk


    #         # チームグループを作成する
    #         team_group = TeamGroup.objects.create(
    #             tournament_id = tournament_id, 
    #             category = 1
    #         )


    #         # チームを保存する
    #         team_group_id = team_group.pk
    #         team_instances = [
    #             Team(team_group=team_group, name=name)
    #             for name in teams  
    #         ]
    #         if team_instances:
    #             Team.objects.bulk_create(team_instances)

            
    #         # 順位ポイントを保存する
    #         rank = 1
    #         points_instances = [
    #             TournamentPoint(tournament_id=tournament_id,   rank=i, point=p)
    #             for i, p in enumerate(points, 1) 
    #         ]
    #         if points_instances:
    #             TournamentPoint.objects.bulk_create(points_instances)

    #     return response
