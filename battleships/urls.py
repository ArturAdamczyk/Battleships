"""battleships URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import TemplateView
from battleships.views import open_game, join_game, new_game, refresh_ui, PlayerListView, sign_up, play

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', sign_up, name='sign_up'),
    path('', PlayerListView.as_view(template_name='home.html'), name='home'),
    path('new_game/', new_game, name='new_game'),
    path('game/<int:game_id>/<slug:game_name>/join', join_game, name='join_game'),
    path('game/<int:game_id>/<slug:game_name>/refresh', refresh_ui, name='refresh_ui'),
    path('game/<int:game_id>/<slug:game_name>', open_game, name="game"),
    #path('game/<int:game_id>/<slug:game_name>/<slug:raw_message>/play', play, name="play"),
    path('game/<int:game_id>/<slug:game_name>/play', play, name="play"),

]
