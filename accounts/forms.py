from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 追加

from .models import User


# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User