from django.urls import path
from .views import EventResultEditView

urlpatterns = [
    # 競技結果の編集
    path('edit', EventResultEditView.as_view(), name='event_result_edit'),

]