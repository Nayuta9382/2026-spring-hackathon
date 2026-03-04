from django.urls import path
from .views import EventCreateView,EventAdminDetailView

urlpatterns = [
    # 大会のID（tournament_pk）を指定して競技を作成するURL
    path('add', EventCreateView.as_view(), name='event_create'),
    # 競技詳細表示する(管理者)
    path('<int:pk>/admin', EventAdminDetailView.as_view(), name='event_detail_admin'),

]