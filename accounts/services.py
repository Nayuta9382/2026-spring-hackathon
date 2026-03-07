import jwt
import datetime
import os
from django.conf import settings
from django.shortcuts import redirect
from functools import wraps

# 秘密鍵の取得
SECRET_KEY = settings.SECRET_KEY

# JWTを作成してCookieに保存する
def create_jwt_and_set_cookie(response):
    # 1. 有効期限の設定
    expiry_hours = int(os.environ.get('JWT_EXPIRY_HOURS', 1))
    now = datetime.datetime.now(datetime.timezone.utc)
    
    payload = {
        'exp': now + datetime.timedelta(hours=expiry_hours),
        'iat': now,
    }
    
    # 2. トークン生成
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # PyJWTのバージョンによりbytesで返る場合があるためstrに変換
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    # 3. responseのCookieにセット
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=expiry_hours * 3600
    )
    return response

# jwtを検証する
def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

# cookie内のjwtを検証する（デコレータ）
def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        
        if not token or not verify_jwt(token):
            from django.urls import reverse
            from urllib.parse import quote
            login_url = reverse('operator_login') 
            return redirect(f"{login_url}?next={quote(request.path)}")
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# jwtをcookieから削除
def logout_user(response):
    response.delete_cookie('access_token')