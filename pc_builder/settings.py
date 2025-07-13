# pc_builder/settings.py
from pathlib import Path
import os
import sys
import pyodbc
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, os.path.join(BASE_DIR, ''))
sys.path.insert(0, os.path.join(BASE_DIR, ''))


load_dotenv()
"""
Загрузка настроек проекта Django.

Этот модуль содержит конфигурацию Django, включая:
- Пути к проекту.
- Загрузку переменных окружения из .env.
- Секретные ключи и настройки отладки.
- Установленные приложения и middleware.
- Настройки шаблонов.
- Настройки базы данных (MSSQL).
- Валидацию паролей.
- Интернационализацию и локализацию.
- Настройки статических и медиа файлов.
- Настройки аутентификации, включая URL для входа и перенаправления.
- Настройки электронной почты (Yandex).
- Настройки кэширования (Redis).
- Настройки логирования.

Использует переменные окружения для большей гибкости и безопасности.
"""

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
DEBUG = True  
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.2', '188.225.127.177'] 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'components',
    'games',
    'builds',
    'users',
    'fps_data',
    'debug_toolbar',
    'widget_tweaks',
    
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'pc_builder.urls'

import os


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pc_builder.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv("DJANGO_DATABASE_NAME", "Games"),
        'USER': os.getenv('DJANGO_DATABASE_USER'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', ''),
        'OPTIONS': {
            'driver': os.getenv(
                'DJANGO_DATABASE_OPTIONS_DRIVER', 'ODBC Driver 17 for SQL Server'
            ),
            'TrustServerCertificate': 'yes',
            'Encrypt': 'optional',
            'instance': os.getenv(
                'DJANGO_DATABASE_OPTIONS_INSTANCE', 'SQLEXPRESS'
            ),
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'  # Или 'ru'
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Europe/Moscow'

INTERNAL_IPS = [
    "127.0.0.1",
    
]
INTERNAL_IPS = ["*"]



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.parent / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'auth.User'




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # Хост Yandex.Mail
EMAIL_PORT = 465  # Порт для SSL (465) или 587 для TLS
EMAIL_USE_TLS = False  # Используйте False для SSL, True для TLS
EMAIL_USE_SSL = True  # Используйте True для SSL, False для TLS
EMAIL_HOST_USER = 'niaz123rezeda123@ya.ru'  # Ваш адрес электронной почты Yandex
EMAIL_HOST_PASSWORD = 'qmcexvaqscmgaiey'  # Пароль от вашей почты Yandex
DEFAULT_FROM_EMAIL = 'niaz123rezeda123@ya.ru'  # От кого будут отправляться письма (ваш адрес)
DEFAULT_CHARSET = 'utf-8'  # или 'utf-8'
import logging

logger = logging.getLogger(__name__)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

try:
    from django.core.cache import cache

    cache.get('test_cache_connection')
except Exception as e:
    logger.error(f"Redis connection error: {e}")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console', 'file'],
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
    },
}
# Настройки кэширования (дополнительно)
CACHE_ENABLED = True  # Читаем из .env
CACHE_MIDDLEWARE_ALIAS = "default"  # Используем кэш по умолчанию
CACHE_MIDDLEWARE_SECONDS =0 # Кэшировать на 15 минут (в секундах)
CACHE_MIDDLEWARE_KEY_PREFIX = ""  # Префикс для ключей кэша # Префикс для ключей кэшаючей кэша

"""
Скрипт для создания базы данных MS SQL Server.

Этот скрипт предназначен для создания базы данных MS SQL Server, если она не существует.
Он использует параметры подключения, указанные в файле .env.
"""
print("СТАРТ")


CACHE_MIDDLEWARE_IGNORE_PATHS = [
    '/builds/cart/',  # Страница корзины
    '/builds/add_to_cart/',  # Добавление в корзину
    '/builds/remove_from_cart/',  # Удаление из корзины
    '/users/login/',  # Страница логина
    '/users/logout/',  # Страница выхода
    '/users/register/',  # Страница регистрации
    '/components/stock_list/',
    '/builds/checkout/',
    '/builds/employee_order_list/',
   
]

CACHE_MIDDLEWARE_KEY_PREFIX = 'employee_order_list_' 
