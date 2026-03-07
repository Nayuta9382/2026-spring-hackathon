from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from .forms import LoginFrom ,OperatorLoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .services import create_jwt_and_set_cookie
from tournaments.services import get_tournament_by_uuid

class IndexView(TemplateView):
    template_name = "index.html"



# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "accounts/login.html"

# 運営者ログイン処理
class OperatorLoginView(FormView):
    template_name = 'accounts/operator-login.html'
    form_class = OperatorLoginForm


    # 最初にログインしようとしていたページへリダイレクト
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        
        # nextが存在し、かつ空文字でない場合はそのURLへ
        if next_url:
            return next_url
            
        # なければデフォルトURLへリダイレクト
        return ('/')

    def form_valid(self, form):
        password = form.cleaned_data['password']
        

        is_valid = False
        # 大会パスワードと一致しているか検証
        # 大会を取得
        tournament = get_tournament_by_uuid('bd1e91b6-6655-4a6c-8f98-a454b43e2c53')
        if tournament.password == password:
            is_valid = True

        # 認証が成功したら
        if is_valid:

            target_url = self.get_success_url()
            
            # 2. ここで初めて Redirect オブジェクトを作る
            response = HttpResponseRedirect(target_url)
            
            # JWTを作成してCookieに保存
            create_jwt_and_set_cookie(response)
            
            return response
        else:
            form.add_error('password', 'パスワードが違います。')
            return self.form_invalid(form)