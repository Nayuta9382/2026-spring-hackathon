from django.urls import path
from .views import EventCreateView,EventEditView,EventAdminDetailView,EventUserDetailView

urlpatterns = [
    # 大会のID（tournament_pk）を指定して競技を作成するURL
    path('add', EventCreateView.as_view(), name='event_create'),
    # 競技詳細(管理者)
    path('<int:pk>/admin', EventAdminDetailView.as_view(), name='event_detail_admin'),
    # 競技詳細(一般)
    path('<int:pk>/user', EventUserDetailView.as_view(), name='event_detail_user'),
    # 競技を編集する
    path('<int:pk>/edit', EventEditView.as_view(), name='event_edit'),

]