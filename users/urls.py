from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('return_request/<int:order_item_id>/', views.create_return_request, name='create_return_request'),
    path('top_up_balance/', views.top_up_balance, name='top_up_balance'),
    path('confirm_top_up/', views.confirm_top_up, name='confirm_top_up'),
]
