from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from .services import is_superuser_authenticated, is_operator_authenticated, is_superuser_session
from django.utils.http import urlencode


# スーパユーザと運営者を認証する
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)




        # スーパユーザとしてログインしているかを認証
        if is_superuser_authenticated(request):
            # 認証されていれば、そのままビューを実行
            return view_func(request, *args, **kwargs)
        # 運営者とログインしているかを認証
        if is_operator_authenticated(request):
            return view_func(request, *args, **kwargs)
        
        # リダイレクトを指定する
        # スーパユーザとしてログイン履歴があれば
        if is_superuser_session(request):
            # スーパユーザのログインページへ
            return redirect('/accounts/login/')
        else:
            # 運営者ログインページへ
            login_url = '/accounts/operator-login/'
            current_path = request.get_full_path()
            return redirect(f"{login_url}?{urlencode({'next': current_path})}")
    return _wrapped_view

# スーパユーザを認証する
def super_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    
        # スーパユーザとしてログインしているかを認証
        if is_superuser_authenticated(request):
            # 認証されていれば、そのままビューを実行
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/accounts/login/')
    return _wrapped_view

# 運営者を認証する
def operator_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)


        # 運営者とログインしているかを認証
        if is_operator_authenticated(request):
            return view_func(request, *args, **kwargs)
        else:
            # 運営者ログインページへ
            login_url = '/accounts/operator-login/'
            current_path = request.get_full_path()
            return redirect(f"{login_url}?{urlencode({'next': current_path})}")
    return _wrapped_view