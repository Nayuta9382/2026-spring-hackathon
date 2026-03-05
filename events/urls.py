from django.urls import path
from .views import EventCreateView,EventEditView,EventAdminDetailView

urlpatterns = [
    # 大会のID（tournament_pk）を指定して競技を作成するURL
    path('add', EventCreateView.as_view(), name='event_create'),
    # 競技詳細
    path('<int:pk>/admin', EventAdminDetailView.as_view(), name='event_detail_admin'),
    # 競技を編集する
    path('<int:pk>/edit', EventEditView.as_view(), name='event_edit'),

]