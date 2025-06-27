# users/utils.py
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_status_email(order):
    """Отправляет email уведомление об изменении статуса заказа."""
    try:
        if order.status == 'delivered':
            subject = f"Ваш заказ #{order.pk} доставлен и ожидает вас!"
            message = (
                f"Здравствуйте, {order.user.username}!\n\n"
                f"Ваш заказ #{order.pk} доставлен и ожидает вас по адресу самовывоза. "
                f"Пожалуйста, заберите его в удобное для вас время.\n\n"
                f"Спасибо за ваш заказ!"
            )
        elif order.status == 'delivering':
            subject = f"Ваш заказ #{order.pk} будет доставлен в течение 3 часов!"
            message = (
                f"Здравствуйте, {order.user.username}!\n\n"
                f"Ваш заказ #{order.pk} находится в процессе доставки и будет доставлен вам в течение 3 часов.\n\n"
                f"Спасибо за ваш заказ!"
            )
        else:
            subject = f"Обновление статуса заказа #{order.pk}"
            message = (
                f"Здравствуйте, {order.user.username}!\n\n"
                f"Статус вашего заказа #{order.pk} был изменен на: "
                f"{order.get_status_display()}.\n\n"
                f"Спасибо за ваш заказ!"
            )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Отправитель (укажите в settings.py)
            [order.email],  # Получатель (email из заказа)
            fail_silently=False,
        )
        print(
            f"DEBUG: Email sent to {order.email} for order #{order.pk}, "
            f"status: {order.status}"
        )  # Логгируем отправку
    except Exception as e:
        print(
            f"DEBUG: Error sending email to {order.email} for order #{order.pk}: {e}"
        )  # Логгируем ошибку


def send_registration_email(user):
    """Отправляет письмо с информацией о регистрации."""
    subject = 'Регистрация на нашем сайте'
    message = render_to_string(
        'users/email/registration_email.txt',
        {
            'user': user,
        },
    )
    html_message = render_to_string(
        'users/email/registration_email.html',
        {
            'user': user,
        },
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email, html_message=html_message)


def send_password_reset_email(user, new_password):
    """Отправляет письмо с новым паролем."""
    subject = 'Сброс пароля'
    message = render_to_string(
        'users/email/password_reset_email.txt',
        {
            'user': user,
            'new_password': new_password,
        },
    )
    html_message = render_to_string(
        'users/email/password_reset_email.html',
        {
            'user': user,
            'new_password': new_password,
        },
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email, html_message=html_message)
