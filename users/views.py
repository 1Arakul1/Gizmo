# users/views.py
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.auth.forms import UserCreationForm  # noqa: F401
from django.contrib.auth.tokens import default_token_generator  # noqa: F401
from django.db import models  # noqa: F401
from django.contrib.auth import authenticate, login  # noqa: F401
from django.db import transaction # Импортируем для транзакций
from django.urls import reverse # Импортируем reverse
from django.conf import settings #Импортируем settings

from builds.models import Build, CartItem, Order, OrderItem, ReturnRequest
from .forms import CustomUserCreationForm, TopUpBalanceForm # Импортируем TopUpBalanceForm
from .models import Balance, Transaction # Импортируем Balance и Transaction
from .utils import (
    send_registration_email,
    send_password_reset_email,
    send_order_status_email,
)
import secrets
import string


@login_required
def profile(request):
    """Отображает профиль пользователя, его сборки, корзину и заказы."""
    user = request.user
    builds = Build.objects.filter(user=user)
    cart_items = CartItem.objects.filter(user=user)
    orders = Order.objects.filter(user=user).order_by('-order_date')
    return_requests = ReturnRequest.objects.filter(user=user)

    # Получаем или создаем баланс пользователя
    balance, created = Balance.objects.get_or_create(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp')  # Получаем историю транзакций

    # Проверяем статус заказов и отправляем уведомления
    for order in orders:
        if order.status in ['delivered', 'delivering']:
            send_order_status_email(order)


    context = {
        'user': user,
        'builds': builds,
        'cart_items': cart_items,
        'orders': orders,
        'return_requests': return_requests,
        'balance': balance,
        'transactions': transactions,  # Передаем историю транзакций в контекст
    }
    return render(request, 'users/profile.html', context)


@login_required
def create_return_request(request, order_item_id):
    print("create_return_request called!")  # Добавляем это
    order_item = get_object_or_404(
        OrderItem, pk=order_item_id, order__user=request.user
    )  # Добавлена проверка пользователя

    # Проверяем, что для этого заказа ещё нет запроса на возврат
    if order_item.order.return_request:
        messages.error(request, "Для этого заказа уже создан запрос на возврат.")
        return redirect('users:profile')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            return_request = ReturnRequest.objects.create(
                user=request.user, order_item=order_item, reason=reason
            )
            order_item.order.return_request = return_request
            order_item.order.save()
            messages.success(request, "Запрос на возврат успешно создан.")  # Добавлено сообщение об успехе
            return redirect('users:profile')  # Перенаправляем обратно в профиль
        else:
            # Обработка случая, когда причина не указана
            return render(
                request,
                'users/return_request_form.html',
                {
                    'order_item': order_item,
                    'error': 'Пожалуйста, укажите причину возврата.',
                },
            )

    return render(request, 'users/return_request_form.html', {'order_item': order_item})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_registration_email(user)  # Send the email
                username = form.cleaned_data.get('username')
                messages.success(
                    request,
                    f'Account created for {username}! An email has been sent to your email.',
                )
                return redirect('users:login')
            except Exception as e:
                messages.error(
                    request, 'Could not send email. Please contact administration.'
                )
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
            send_password_reset_email(user, new_password)  # Используем новую функцию
            messages.success(request, 'Новый пароль отправлен на ваш email.')
            return redirect('users:login')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден.')
            return render(request, 'users/password_reset.html')
    return render(request, 'users/password_reset.html')

@login_required
def top_up_balance(request):
    """Пополнение баланса пользователя."""
    if request.method == 'POST':
        form = TopUpBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user

            try:
                with transaction.atomic(): # Используем транзакцию
                    balance, created = Balance.objects.get_or_create(user=user)
                    balance.balance += amount
                    balance.save()
                    # Создаем запись в истории транзакций
                    Transaction.objects.create(
                        user=user,
                        amount=amount,
                        transaction_type='deposit',
                        description=f"Пополнение баланса на сумму {amount}",
                    )
                messages.success(request, f"Баланс успешно пополнен на {amount}!")
                return redirect('users:profile')  # Перенаправляем в профиль
            except Exception as e:
                messages.error(request, f"Ошибка при пополнении баланса: {e}")
                print(f"Ошибка пополнения баланса: {e}")
    else:
        form = TopUpBalanceForm()
    return render(request, 'users/top_up_balance.html', {'form': form})