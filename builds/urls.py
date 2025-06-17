from django.urls import path
from . import views

app_name = 'builds'  # **ВАЖНО!**

urlpatterns = [
    path('create/', views.build_create, name='build_create'),
    path('', views.build_list, name='build_list'),
    path('<int:pk>/', views.build_detail, name='build_detail'),
    
    path('<int:pk>/edit/', views.build_edit, name='build_edit'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('employee/orders/', views.employee_order_list, name='employee_order_list'),
    path('employee/orders/<int:order_id>/update/', views.employee_order_update, name='employee_order_update'),
    path('employee/orders/<int:order_id>/complete/', views.employee_order_complete, name='employee_order_complete'),
    path('employee/orders/history/', views.employee_order_history, name='employee_order_history'),
    path('get_compatible_motherboards/', views.get_compatible_motherboards, name='get_compatible_motherboards'),
    path('get_compatible_rams/', views.get_compatible_rams, name='get_compatible_rams'),
    path('get_compatible_cpu/', views.get_compatible_cpu, name='get_compatible_cpu'),



  
   
    path('employee/returns/', views.employee_return_requests, name='employee_return_requests'),
    path('employee/returns/<int:return_request_id>/', views.employee_process_return, name='employee_process_return'),
    
]


