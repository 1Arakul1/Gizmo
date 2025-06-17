from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_registration_email(user):
    """Отправляет письмо с информацией о регистрации."""
    subject = 'Регистрация на нашем сайте'
    message = render_to_string(
        'users/email/registration_email.txt',
        {
            'user': user,
        }
    )
    html_message = render_to_string(
        'users/email/registration_email.html',
        {
            'user': user,
        }
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
        }
    )
    html_message = render_to_string(
        'users/email/password_reset_email.html',
        {
            'user': user,
            'new_password': new_password,
        }
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email, html_message=html_message)