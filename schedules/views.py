from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from events.models import Event
from .models import Schedule


# =========================================
# ヘルパー関数
# =========================================

def get_event(event_pk):
    """イベントをpkで取得する"""
    return get_object_or_404(Event, pk=event_pk)


def get_schedules(event):
    """イベントに紐づくスケジュール一覧を取得する"""
    return event.schedules.all()


def get_schedules_by_status(event):
    """スケジュールをstatus別に分けて返す"""
    schedules = get_schedules(event)
    return {
        'next_schedules': schedules.filter(status=0),
        'now_schedules': schedules.filter(status=1),
        'previous_schedules': schedules.filter(status=2),
    }


def build_success_url(event_pk):
    """成功時のリダイレクトURL（schedule_editに戻る）"""
    from django.urls import reverse
    return reverse('schedule_edit', kwargs={'pk': event_pk})


def delete_schedules(request, event):
    """チェックされたスケジュールを削除する"""
    delete_ids = request.POST.getlist('delete_ids')
    get_schedules(event).filter(pk__in=delete_ids).delete()


def save_existing_schedules(request, event):
    """既存スケジュールを更新する"""
    for schedule in get_schedules(event):
        schedule.detail = request.POST.get(f'detail_{schedule.pk}', schedule.detail)
        schedule.result = request.POST.get(f'result_{schedule.pk}', schedule.result)
        schedule.status = int(request.POST.get(f'status_{schedule.pk}', schedule.status))
        schedule.order = int(request.POST.get(f'order_{schedule.pk}', schedule.order))
        schedule.save()


def create_new_schedules(request, event):
    """新規スケジュールを作成する"""
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
                order=int(order) if order else 0,
            )


# =========================================
# ビュー
# =========================================

class ScheduleListView(View):
    """スケジュールをnext/now/previousで分けて一覧表示するビュー"""
    template_name = 'schedules/edit.html'

    def get(self, request, pk):
        event = get_event(pk)
        context = get_schedules_by_status(event)
        context['event'] = event
        return render(request, self.template_name, context)


class ScheduleUpdateView(View):
    """スケジュールの一覧表示・追加・更新・削除を担当するビュー"""
    template_name = 'schedules/edit.html'

    def get(self, request, pk):
        event = get_event(pk)
        context = get_schedules_by_status(event)
        context['event'] = event
        context['schedules'] = get_schedules(event)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        event = get_event(pk)
        delete_schedules(request, event)
        save_existing_schedules(request, event)
        create_new_schedules(request, event)
        return redirect(build_success_url(pk))
