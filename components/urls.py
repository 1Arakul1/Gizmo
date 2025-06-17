# components/urls.py

from django.urls import path
from . import views

app_name = 'components'

urlpatterns = [
    path('cpus/', views.cpu_list, name='cpu_list'),
    path('cpus/<int:pk>/', views.cpu_detail, name='cpu_detail'),
    path('stock/', views.stock_list_view, name='stock_list'),
    
    path('stock/replenish/<int:pk>/', views.replenish_stock_item, name='replenish_stock_item'),
    path('stock/reduce/<int:pk>/', views.reduce_stock_item, name='reduce_stock_item'),

    path('gpus/', views.gpu_list, name='gpu_list'),
    path('gpus/<int:pk>/', views.gpu_detail, name='gpu_detail'),

    path('motherboards/', views.motherboard_list, name='motherboard_list'),
    path('motherboards/<int:pk>/', views.motherboard_detail, name='motherboard_detail'),

    path('rams/', views.ram_list, name='ram_list'),
    path('rams/<int:pk>/', views.ram_detail, name='ram_detail'),

    path('storages/', views.storage_list, name='storage_list'),
    path('storages/<int:pk>/', views.storage_detail, name='storage_detail'),

    path('psus/', views.psu_list, name='psu_list'),
    path('psus/<int:pk>/', views.psu_detail, name='psu_detail'),

    path('cases/', views.case_list, name='case_list'),
    path('cases/<int:pk>/', views.case_detail, name='case_detail'),
    path('coolers/', views.cooler_list, name='cooler_list'),
    path('coolers/<int:pk>/', views.cooler_detail, name='cooler_detail'),
    
]