from django.shortcuts import render
from django.views.generic import View
from .models import EventResult
from django.shortcuts import get_object_or_404,render, redirect
from django.urls import reverse_lazy
from .services import get_event_results_by_event_id
from .forms import EventResultForm
from .models import EventResult
from django.forms import modelformset_factory
from events.service import get_event_by_id,get_event_by_id
from teams.service import get_team_group_by_event
from tournaments.services import get_rank_point_by_event,get_rank_points_by_event
import json

# Formsetを定義
EventResultFormSet = modelformset_factory(EventResult, form=EventResultForm, extra=0)


# 競技結果を編集する
class EventResultEditView(View):
    template_name = 'event-results/edit.html'

    # 競技結果を表示する(formset)
    def get(self, request, **kwargs):
        # 競技idを取得
        event_id = self.kwargs['event_pk']
        # 競技のオブジェクトを取得
        event = get_event_by_id(event_id=event_id)

        # 競技結果の一覧を取得し渡す
        event_results = get_event_results_by_event_id(event_id=event_id)
        queryset = get_event_results_by_event_id(event_id=event_id)
        formset = EventResultFormSet(queryset=queryset)

        # チームグループオブジェクトを取得する
        team_group = get_team_group_by_event(event_id)

        # 大会ポイントの一覧を取得する
        tournament_points =  get_rank_points_by_event(event=event)
        # jsonに変換
        points_dict = {tp.rank: tp.point for tp in tournament_points }
        tournament_points_json = json.dumps(points_dict)

        return render(request, self.template_name, {'formset': formset,'team_group' : team_group,'event' : event, 'tournament_points' : tournament_points,'tournament_points_json' : tournament_points_json})
        
        
    # 競技結果を一件ずつ保存していく
    def post(self, request, **kwargs):
        # データを受け取りformを復元する(データの紐づけ)
        event_id = self.kwargs['event_pk']
        queryset = get_event_results_by_event_id(event_id=event_id)
        formset = EventResultFormSet(request.POST,queryset=queryset)
        event = get_event_by_id(event_id=event_id)
        # バリデーションエラーの場合
        if not formset.is_valid():
            return render(request, self.template_name, {'formset': formset})

        # クラス順位ポイントを使用するかどうか
        class_team_flg = "0"
        team_group = get_team_group_by_event(event_id)
        # クラス競技でなら使用
        if(team_group.category == 1):
            class_team_flg = request.POST.get('class-team-flg')
        else:
            class_team_flg = "0"
            

        # オブジェクトを受け取る
        instances = formset.save(commit=False)
        event.is_class_point = (class_team_flg == "1")
        event.save()
        # データの保存
        for form in formset.forms:
            instance = form.instance
            rank_point = 0
            # クラスポイントを使用するなら
            if class_team_flg == "1": 
                rank = instance.rank
                # クラスポイントを取得する
                rank_point = get_rank_point_by_event(event=event,rank=rank)
            else : 
                rank_point = instance.point

            # 使用するポイントを修正
            instance.point = rank_point
            
            # 保存
            instance.save()

      
        # 今のページにリダイレクト
        return redirect('event_result_edit', 
            tournament_pk=event.tournament.id, 
            event_pk=event.id
        )
        
  