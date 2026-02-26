from django.urls import path
from django.contrib.auth import views as auth_views # 名前が被らないように変更
from . import views  # 自分のアプリの views.py を読み込む

app_name = 'accounts'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('login/', views.LoginView.as_view(), name="login"),
]