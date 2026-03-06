from django.shortcuts import render
from django.views.generic import View
from .models import EventResult
from django.shortcuts import get_object_or_404,render, redirect
from django.urls import reverse_lazy
from .services import get_event_results_by_event_id
from .forms import EventResultForm
from .models import EventResult
from django.forms import modelformset_factory
from events.service import get_event_by_id

# Formsetを定義
EventResultFormSet = modelformset_factory(EventResult, form=EventResultForm, extra=0)


# 競技結果を編集する
class EventResultEditView(View):
    template_name = 'event-results/edit.html'

    # 競技結果を表示する(formset)
    def get(self, request, **kwargs):
        # 競技idを取得
        event_id = self.kwargs['event_pk']
        # 競技結果の一覧を取得し渡す
        event_results = get_event_results_by_event_id(event_id=event_id)
        queryset = get_event_results_by_event_id(event_id=event_id)
        formset = EventResultFormSet(queryset=queryset)
        return render(request, self.template_name, {'formset': formset})
        
    # 競技結果を一件ずつ保存していく
    def post(self, request, **kwargs):
        # データを受け取りformを復元する(データの紐づけ)
        event_id = self.kwargs['event_pk']
        queryset = get_event_results_by_event_id(event_id=event_id)
        formset = EventResultFormSet(request.POST,queryset=queryset)
        # バリデーションエラーの場合
        if not formset.is_valid():
            return render(request, self.template_name, {'formset': formset})

        class_team_flg = request.POST.get('class-team-flg')
        print(f"選択された値: {class_team_flg}") # "1" か "0" が入る

        # オブジェクトを受け取る
        instances = formset.save(commit=False)
        # データの保存
        for instance in instances:
            # ここで instance（EventResultモデルの卵）を操作できます
            # 例: instance.updated_by = request.user 
            print(f"保存処理中: ID={instance.id}, 順位={instance.rank}")
            
            # 保存
            instance.save()

        event = get_event_by_id(event_id=event_id)
        # 今のページにリダイレクト
        return redirect('event_result_edit', 
            tournament_pk=event.tournament.id, 
            event_pk=event.id
        )
        
  