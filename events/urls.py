from django.urls import path
from .views import EventCreateView

urlpatterns = [
    # 大会のID（tournament_pk）を指定して競技を作成するURL
    path('add', EventCreateView.as_view(), name='event_create'),
]