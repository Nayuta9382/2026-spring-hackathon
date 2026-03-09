from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 追加
from django import forms

from .models import User


# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User

# 運営者用のログインフォームを表示
class OperatorLoginForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)