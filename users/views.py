# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from builds.models import Build, CartItem
from .utils import send_registration_email, send_password_reset_email  # Добавляем импорт
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
import secrets # Импортируем secrets
import string # Импортируем string
from .utils import send_registration_email  # Import the email function
from django.contrib.auth import authenticate, login  # Import login
from django.contrib.auth import get_user_model  # Get the User model
from builds.models import Build, CartItem, Order
from builds.models import Build, CartItem, Order, OrderItem, ReturnRequest
from django.db import models


from django.db import models # Импортируем models

@login_required
def profile(request):
    """Отображает профиль пользователя, его сборки, корзину и заказы."""
    user = request.user
    builds = Build.objects.filter(user=user)
    cart_items = CartItem.objects.filter(user=user)

    # Получаем ВСЕ заказы пользователя, сортированные по дате
    orders = Order.objects.filter(user=user).order_by('-order_date')

    return_requests = ReturnRequest.objects.filter(user=user)

    context = {
        'user': user,
        'builds': builds,
        'cart_items': cart_items,
        'orders': orders,
        'return_requests': return_requests,
    }
    return render(request, 'users/profile.html', context)


@login_required
def create_return_request(request, order_item_id):
    print("create_return_request called!")  # Добавляем это
    order_item = get_object_or_404(OrderItem, pk=order_item_id, order__user=request.user) # Добавлена проверка пользователя

    # Проверяем, что для этого заказа ещё нет запроса на возврат
    if order_item.order.return_request:
        messages.error(request, "Для этого заказа уже создан запрос на возврат.")
        return redirect('users:profile')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            return_request = ReturnRequest.objects.create(user=request.user, order_item=order_item, reason=reason)
            order_item.order.return_request = return_request
            order_item.order.save()
            messages.success(request, "Запрос на возврат успешно создан.")  # Добавлено сообщение об успехе
            return redirect('users:profile')  # Перенаправляем обратно в профиль
        else:
            # Обработка случая, когда причина не указана
            return render(request, 'users/return_request_form.html', {'order_item': order_item, 'error': 'Пожалуйста, укажите причину возврата.'})

    return render(request, 'users/return_request_form.html', {'order_item': order_item})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_registration_email(user)  # Send the email
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}! An email has been sent to your email.')
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f'Could not send email. Please contact administration.')
                print(f"Error sending registration email: {e}")
                user.delete()
                return render(request, 'users/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            # Генерируем случайный пароль
            alphabet = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(secrets.choice(alphabet) for i in range(12))
            # Устанавливаем новый пароль
            user.set_password(new_password)
            user.save()
            # Отправляем письмо с новым паролем
            send_password_reset_email(user, new_password) # Используем новую функцию
            messages.success(request, 'Новый пароль отправлен на ваш email.')
            return redirect('users:login')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден.')
            return render(request, 'users/password_reset.html')
    return render(request, 'users/password_reset.html')