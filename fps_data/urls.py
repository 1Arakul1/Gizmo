# fps_data/urls.py

from django.urls import path
from . import views

app_name = 'fps_data'

urlpatterns = [
    # Пример: список данных FPS (может быть полезно для отладки)
    path('', views.fps_data_list, name='fps_data_list'),
    # Пример: детальная информация о данных FPS для конкретной игры и компонентов
    path('<int:game_id>/<int:cpu_id>/<int:gpu_id>/', views.fps_data_detail, name='fps_data_detail'),
    # Другие URL для работы с данными FPS
]