from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('list-games', views.list_games_view, name='list-games'),
    path('create-game', views.create_game_view, name='create-game'),
    path('ready-player', views.ready_player_view, name='/ready-player'),
    path('board', views.board_view, name='/board'),
    path('go-back', views.go_back_view, name='/go-back'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('update',views.json_board_state, name='update'),
    
]