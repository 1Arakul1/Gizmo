# games/urls.py

from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('<int:pk>/', views.game_detail, name='game_detail'),
    path('predict_fps/', views.predict_fps, name='predict_fps'), #Добавляем предсказания для FPS
    path('<int:pk>/', views.game_detail, name='game_detail'),
]