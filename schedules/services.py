from .models import Schedule

def get_schedules_by_event(event):
    return event.schedules.all().order_by('order')

def get_now_schedules_by_event(event):
    return get_schedules_by_event(event).filter(status=0)

def get_next_schedules_by_event(event):
    return get_schedules_by_event(event).filter(status=1)

def get_previous_schedules_by_event(event):
    return get_schedules_by_event(event).filter(status=2)

# POSTデータのnowが2個以上ないか確認する
def validate_now_count(event, post_data):
    schedules = list(get_schedules_by_event(event))
    delete_ids = post_data.getlist('delete_ids')

    now_count = 0

    # 既存スケジュールのnow件数をカウント
    for s in schedules:
        if str(s.pk) in delete_ids:
            continue
        status = int(post_data.get(f'status_{s.pk}', s.status))
        if status == 0:
            now_count += 1

    # 新規追加のnow件数をカウント
    new_statuses = post_data.getlist('new_status')
    new_details = post_data.getlist('new_detail')
    for detail, status in zip(new_details, new_statuses):
        if detail and int(status) == 0:
            now_count += 1

    return now_count <= 1

# 指定されたIDのスケジュールをDBから削除する
def delete_schedules_by_ids(event, delete_ids):
    if delete_ids:
        event.schedules.filter(pk__in=delete_ids).delete()


# 既存スケジュールを更新するs
def update_schedules_by_event(event, post_data):
    schedules = list(get_schedules_by_event(event))

    for s in schedules:
        Schedule.objects.filter(pk=s.pk).update(order=s.pk + 100000)

    for s in schedules:
        Schedule.objects.filter(pk=s.pk).update(
            detail=post_data.get(f'detail_{s.pk}', s.detail),
            result=post_data.get(f'result_{s.pk}', s.result),
            status=int(post_data.get(f'status_{s.pk}', s.status)),
            order=int(post_data.get(f'order_{s.pk}', s.order)),
        )


# 新規スケジュールを作成する
def create_schedules_by_post(event, post_data):
    new_details = post_data.getlist('new_detail')
    new_results = post_data.getlist('new_result')
    new_statuses = post_data.getlist('new_status')
    new_orders = post_data.getlist('new_order')

    for detail, result, status, order in zip(new_details, new_results, new_statuses, new_orders):
        if detail:
            Schedule.objects.create(
                event=event,
                detail=detail,
                result=result,
                status=int(status) if status else 0,
                order=int(order) if order else 1,
            )
