from django.urls import path
from .views import EventCreateView,EventEditView,EventAdminDetailView,EventUserDetailView,EventDeleteView,EventResultsAPIView
from accounts.decorators import admin_required


urlpatterns = [
    # 大会のID（tournament_pk）を指定して競技を作成するURL
    path('add', admin_required(EventCreateView.as_view()), name='event_create'),
    # 競技詳細(管理者)
    path('<int:pk>/admin', admin_required(EventAdminDetailView.as_view()), name='event_detail_admin'),
    # 競技詳細(一般)
    path('<int:pk>/user', EventUserDetailView.as_view(), name='event_detail_user'),
    # 競技を編集する
    path('<int:pk>/edit', admin_required(EventEditView.as_view()), name='event_edit'),
    # 競技削除
    path('<int:pk>/delete',admin_required(EventDeleteView.as_view()),name='event_delete'),
    # 競技結果取得
    path('<int:pk>/api/results', EventResultsAPIView.as_view(), name='event_results_api'),
]

