from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse
from django.db import transaction
from events.models import Event
from .models import Schedule

def update_event_schedules_after(request, event):
    """
    イベントに紐づくスケジュールの一括更新・削除・新規作成を行う
    """
    # 1. 削除処理
    delete_ids = request.POST.getlist('delete_ids')
    if delete_ids:
        event.schedules.filter(pk__in=delete_ids).delete()

    # 2. 既存スケジュールの更新処理
    schedules = list(event.schedules.all())
    for s in schedules:
        Schedule.objects.filter(pk=s.pk).update(order=s.order + 10000)

    for s in schedules:
        new_detail = request.POST.get(f'detail_{s.pk}', s.detail)
        new_result = request.POST.get(f'result_{s.pk}', s.result)
        new_status = int(request.POST.get(f'status_{s.pk}', s.status))
        new_order = int(request.POST.get(f'order_{s.pk}', s.order))

        Schedule.objects.filter(pk=s.pk).update(
            detail=new_detail,
            result=new_result,
            status=new_status,
            order=new_order,
        )

    # 3. 新規スケジュールの作成処理
    new_details = request.POST.getlist('new_detail')
    new_results = request.POST.getlist('new_result')
    new_statuses = request.POST.getlist('new_status')
    new_orders = request.POST.getlist('new_order')

    for detail, result, status, order in zip(new_details, new_results, new_statuses, new_orders):
        if detail:
            Schedule.objects.create(
                event=event,
                detail=detail,
                result=result,
                status=int(status) if status else 0,
                order=int(order) if order else 1,
            )

# スケジュールを一覧表示する
class ScheduleListView(generic.DetailView):
    model = Event
    template_name = 'schedules/edit.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object

        schedules = event.schedules.all().order_by('order')
        # 数値定義に合わせてフィルタリング (now=0, next=1, previous=2)
        context['now_schedules'] = schedules.filter(status=0)
        context['next_schedules'] = schedules.filter(status=1)
        context['previous_schedules'] = schedules.filter(status=2)

        return context


# スケジュールを一括編集する
class ScheduleUpdateView(generic.UpdateView):
    model = Event
    template_name = 'schedules/edit.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object

        schedules = event.schedules.all().order_by('order')
        # 数値定義に合わせてフィルタリング (now=0, next=1, previous=2)
        context['now_schedules'] = schedules.filter(status=0)
        context['next_schedules'] = schedules.filter(status=1)
        context['previous_schedules'] = schedules.filter(status=2)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event = self.object
        try:
            with transaction.atomic():
                update_event_schedules_after(request, event)
            return redirect(self.get_success_url())
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'保存中にエラーが発生しました: {e}'
            return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('event_detail_admin', kwargs={
            'tournament_pk': self.object.tournament.url_uuid,
            'pk': self.object.pk,
        })