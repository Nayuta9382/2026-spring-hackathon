from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from .forms import LoginFrom # ログインフォームをimport


class IndexView(TemplateView):
    template_name = "index.html"



# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "accounts/login.html"

