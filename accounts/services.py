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

# cookie内のjwtを検証する
def is_authenticated_jwt(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return False
    return verify_jwt(token) 

# jwtをcookieから削除
def logout_user(response):
    response.delete_cookie('access_token')


# スーパユーザとしてログインしているかを検知する
def is_superuser_authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False
# 運営者としてログインしているかを検知する
def is_operator_authenticated(request):
    if is_authenticated_jwt():
        return True
    else:
        return False

# スーパユーザのセッションidが存在していたがどうか
def is_superuser_session(request):
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    if session_key:
        return True
    else:
        return False
