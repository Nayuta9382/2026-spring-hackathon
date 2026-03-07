from django.urls import path
from .views import EventResultEditView
from accounts.decorators import admin_required


urlpatterns = [
    # 競技結果の編集
    path('edit', admin_required(EventResultEditView.as_view()), name='event_result_edit'),

]