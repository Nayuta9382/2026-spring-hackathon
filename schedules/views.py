from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse
from django.db import transaction
from events.models import Event
from .services import (
    get_schedules_by_event,
    get_now_schedules_by_event,
    get_next_schedules_by_event,
    get_previous_schedules_by_event,
    delete_schedules_by_ids,
    update_schedules_by_event,
    create_schedules_by_post,
    validate_now_count,
)


# スケジュールを一覧表示する
class ScheduleListView(generic.DetailView):
    model = Event
    template_name = 'schedules/edit.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['schedules'] = get_schedules_by_event(event)
        context['now_schedules'] = get_now_schedules_by_event(event)
        context['next_schedules'] = get_next_schedules_by_event(event)
        context['previous_schedules'] = get_previous_schedules_by_event(event)
        return context


# スケジュールを一括編集する
class ScheduleUpdateView(generic.UpdateView):
    model = Event
    template_name = 'schedules/edit.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context['schedules'] = get_schedules_by_event(event)
        context['now_schedules'] = get_now_schedules_by_event(event)
        context['next_schedules'] = get_next_schedules_by_event(event)
        context['previous_schedules'] = get_previous_schedules_by_event(event)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event = self.object

        # nowが2個以上ないかチェック
        if not validate_now_count(event, request.POST):
            context = self.get_context_data()
            context['error'] = 'nowが2個以上あります。nowは1つだけ設定してください。'
            return render(request, self.template_name, context)

        try:
            with transaction.atomic():
                delete_schedules_by_ids(event, request.POST.getlist('delete_ids'))
                update_schedules_by_event(event, request.POST)
                create_schedules_by_post(event, request.POST)
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
