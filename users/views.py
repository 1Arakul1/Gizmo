# users/views.py
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
import secrets
import string
import random
from .forms import CustomUserCreationForm, TopUpBalanceForm, ConfirmTopUpForm
from .models import Balance, Transaction
from .utils import (
    send_registration_email,
    send_password_reset_email,
    send_order_status_email,
)
from builds.models import Build, CartItem, Order, OrderItem, ReturnRequest
from decimal import Decimal

@login_required
def profile(request):
    """Отображает профиль пользователя, его сборки, корзину и заказы."""
    user = request.user
    builds = Build.objects.filter(user=user)
    cart_items = CartItem.objects.filter(user=user)
    orders = Order.objects.filter(user=user).order_by('-order_date')
    return_requests = ReturnRequest.objects.filter(user=user)

    balance, created = Balance.objects.get_or_create(user=user)
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp')

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
        'transactions': transactions,
    }
    return render(request, 'users/profile.html', context)

@login_required
def create_return_request(request, order_item_id):
    """Создает запрос на возврат для конкретного заказа."""
    order_item = get_object_or_404(OrderItem, pk=order_item_id, order__user=request.user)

    if order_item.order.return_request:
        messages.error(request, "Для этого заказа уже создан запрос на возврат.")
        return redirect('users:profile')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            return_request = ReturnRequest.objects.create(user=request.user, order_item=order_item, reason=reason)
            order_item.order.return_request = return_request
            order_item.order.save()
            messages.success(request, "Запрос на возврат успешно создан.")
            return redirect('users:profile')
        else:
            return render(request, 'users/return_request_form.html', {
                'order_item': order_item,
                'error': 'Пожалуйста, укажите причину возврата.',
            })

    return render(request, 'users/return_request_form.html', {'order_item': order_item})

def register(request):
    """Регистрирует нового пользователя."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_registration_email(user)
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}! An email has been sent to your email.')
                return redirect('users:login')
            except Exception as e:
                messages.error(request, 'Could not send email. Please contact administration.')
                print(f"Error sending registration email: {e}")
                user.delete()
                return render(request, 'users/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def password_reset(request):
    """Сбрасывает пароль пользователя."""
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            alphabet = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(secrets.choice(alphabet) for i in range(12))
            user.set_password(new_password)
            user.save()
            send_password_reset_email(user, new_password)
            messages.success(request, 'Новый пароль отправлен на ваш email.')
            return redirect('users:login')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден.')
            return render(request, 'users/password_reset.html')
    return render(request, 'users/password_reset.html')

def generate_confirmation_code():
    """Генерирует 6-значный код подтверждения."""
    return str(random.randint(100000, 999999))

@login_required
def top_up_balance(request):
    """Пополнение баланса пользователя."""
    if request.method == 'POST':
        form = TopUpBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            email = form.cleaned_data['email']

            confirmation_code = generate_confirmation_code()
            request.session['confirmation_code'] = confirmation_code
            request.session['top_up_amount'] = float(amount)
            request.session['top_up_email'] = email
            request.session['user_id'] = request.user.id

            print(f"Код подтверждения: {confirmation_code}")
            print("Собираюсь отправить email...")
            send_confirmation_email(email, amount, confirmation_code)
            print("Email отправлен (или должна была быть отправка)")

            messages.info(request, "На вашу электронную почту отправлен код подтверждения. Пожалуйста, введите его.")
            return redirect('users:confirm_top_up')
        else:
            print("Форма НЕ прошла валидацию")
            print(form.errors)
            return render(request, 'users/top_up_balance.html', {'form': form})

    else:
        form = TopUpBalanceForm()
    return render(request, 'users/top_up_balance.html', {'form': form})

@login_required
def confirm_top_up(request):
    """Подтверждение пополнения баланса с использованием кода."""
    if request.method == 'POST':
        form = ConfirmTopUpForm(request.POST)
        if form.is_valid():
            confirmation_code = form.cleaned_data['confirmation_code']
            session_code = request.session.get('confirmation_code')
            amount = request.session.get('top_up_amount')
            email = request.session.get('top_up_email')
            user_id = request.session.get('user_id')

            if confirmation_code == session_code:
                try:
                    with transaction.atomic():
                        user = request.user
                        balance, created = Balance.objects.get_or_create(user=user)
                        amount = Decimal(str(amount))  # Преобразуем amount в Decimal
                        balance.balance += amount
                        balance.save()
                        Transaction.objects.create(
                            user=user,
                            amount=amount,
                            transaction_type='deposit',
                            description=f"Пополнение баланса на сумму {amount}",
                        )

                    messages.success(request, f"Баланс успешно пополнен на {amount}!")

                    del request.session['confirmation_code']
                    del request.session['top_up_amount']
                    del request.session['top_up_email']
                    del request.session['user_id']

                    return redirect('users:profile')
                except Exception as e:
                    messages.error(request, f"Ошибка при пополнении баланса: {e}")
                    print(f"Ошибка пополнения баланса: {e}")
                    return redirect('users:top_up_balance')
            else:
                messages.error(request, "Неверный код подтверждения.")
                return render(request, 'users/confirm_top_up.html', {'form': form, 'error': True})
        else:
            return render(request, 'users/confirm_top_up.html', {'form': form, 'error': True})

    else:
        form = ConfirmTopUpForm()
        return render(request, 'users/confirm_top_up.html', {'form': form})
    
def send_confirmation_email(user_email, amount, confirmation_code):
    """Отправляет email с кодом подтверждения."""
    print(f"send_confirmation_email вызвана с user_email={user_email}, amount={amount}, confirmation_code={confirmation_code}")
    subject = 'Подтверждение пополнения баланса'
    message = f'Для подтверждения пополнения баланса на сумму {amount}, пожалуйста, введите следующий код: {confirmation_code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
    print("Письмо отправлено (или должна была быть отправка)")
