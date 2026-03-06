"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# register_converter を追加
from django.urls import path, include, register_converter
from django.conf import settings
from django.conf.urls.static import static

from .converters import TournamentURLConverter

# コンバーターの登録
register_converter(TournamentURLConverter, 't_url')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tournaments/', include('tournaments.urls')),
    path('tournaments/<t_url:tournament_pk>/events/', include('events.urls')),
    path('tournaments/<t_url:tournament_pk>/events/<event_pk>/event_results/', include('event_results.urls')),
    path('tournaments/schedules/', include('schedules.urls')),
    path('pages/', include('pages.urls')), # 開発中htmlを表示するようのアプリ
]


# 開発環境のみメディアファイルをサーブする設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)