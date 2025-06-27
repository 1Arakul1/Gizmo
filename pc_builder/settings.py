#settings.py - просто нужно будет подставить всё нужное под мой проект.
from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, os.path.join(BASE_DIR, ''))
sys.path.insert(0, os.path.join(BASE_DIR, ''))

# Load environment variables from .env file
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
# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
DEBUG = True
  # В production должно быть False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.2', '188.225.120.28']  # Замени на свой IP

# Application definition
# settings.py

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
    
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
     # **Убедитесь, что он здесь**
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# settings.py

ROOT_URLCONF = 'pc_builder.urls'  # Убедись, что это правильно!

import os


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Важно! Укажите путь к директории с шаблонами
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
# settings.py

WSGI_APPLICATION = 'pc_builder.wsgi.application'  # Убедись, что это правильно!

# Database
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv("DJANGO_DATABASE_NAME", "Games"),
        'USER': os.getenv('DJANGO_DATABASE_USER'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', ''),
        'OPTIONS': {
            'driver': os.getenv('DJANGO_DATABASE_OPTIONS_DRIVER', 'ODBC Driver 17 for SQL Server'),
            'TrustServerCertificate': 'yes',
            'Encrypt': 'optional',
            'instance': os.getenv('DJANGO_DATABASE_OPTIONS_INSTANCE', 'SQLEXPRESS'),
        },
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'ru-RU'  # Или 'ru'
USE_I18N = True
USE_L10N = True # Рекомендуется True для локализации
TIME_ZONE = 'Europe/Moscow'  # Ваш часовой пояс  # Или ваш часовой пояс, например 'Europe/Moscow'

INTERNAL_IPS = [
    "127.0.0.1",
    # "192.168.1.1",  # Замените на свой IP-адрес или используйте '*'
]
INTERNAL_IPS = ["*"]


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # Важно, чтобы начинался и заканчивался слэшем
STATICFILES_DIRS = [
    BASE_DIR.parent / 'static',  # Используй .parent, чтобы подняться на уровень выше
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для сбора статики для продакшена

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'  # URL для доступа к медиафайлам
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Путь к папке для сохранения медиафайлов

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py
LOGIN_URL = 'users:login' #  Используем имя URL из urls.py приложения users
LOGIN_REDIRECT_URL = '/'  # Или другое значение
AUTH_USER_MODEL = 'auth.User'
# settings.py

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # Хост Yandex.Mail
EMAIL_PORT = 465  # Порт для SSL (465) или 587 для TLS
EMAIL_USE_TLS = False #  Используйте False для SSL, True для TLS
EMAIL_USE_SSL = True # Используйте True для SSL, False для TLS
EMAIL_HOST_USER = 'niaz123rezeda123@ya.ru'  # Ваш адрес электронной почты Yandex
EMAIL_HOST_PASSWORD = 'qmcexvaqscmgaiey'  # Пароль от вашей почты Yandex
DEFAULT_FROM_EMAIL = 'niaz123rezeda123@ya.ru'  # От кого будут отправляться письма (ваш адрес)
DEFAULT_CHARSET = 'utf-8'  # или 'utf-8'
import logging
logger = logging.getLogger(__name__)

# Пример
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
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
            'level': 'WARNING',  # ИЗМЕНИТЕ ЗДЕСЬ
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
CACHE_MIDDLEWARE_SECONDS = 10  # Кэшировать на 15 минут (в секундах)
CACHE_MIDDLEWARE_KEY_PREFIX = ""  # Префикс для ключей кэша # Префикс для ключей кэшаючей кэша

#!/usr/bin/env python
"""
Скрипт для создания базы данных MS SQL Server.

Этот скрипт предназначен для создания базы данных MS SQL Server, если она не существует.
Он использует параметры подключения, указанные в файле .env.
"""
print ("СТАРТ")
import os
import pyodbc
from dotenv import load_dotenv

def create_database():
    """
    Создает базу данных MS SQL Server, если она не существует.
    
    Считывает параметры подключения из переменных окружения, загруженных из .env файла.
    Проверяет, существует ли база данных с указанным именем, и, если нет, создает ее.
    """
    load_dotenv()

    db_name = os.getenv("DJANGO_DATABASE_NAME", "")  # Имя базы данных из env, по умолчанию "Bony"
    db_user = os.getenv("DJANGO_DATABASE_USER")
    db_password = os.getenv("DJANGO_DATABASE_PASSWORD")
    db_host = os.getenv("DJANGO_DATABASE_HOST")

    if not all([db_user, db_password, db_host]):
        print("Ошибка: Не все необходимые переменные окружения установлены.")
        return

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};UID={db_user};PWD={db_password}'
    cnxn = None

    try:
        cnxn = pyodbc.connect(connection_string, autocommit=True)
        cursor = cnxn.cursor()

        # Проверяем, существует ли база данных
        cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{db_name}'")
        result = cursor.fetchone()

        if result:
            print(f"База данных '{db_name}' уже существует.")
            return

        # Создаем базу данных
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"База данных '{db_name}' успешно создана.")

    except pyodbc.Error as ex:
        print(f"Ошибка при создании базы данных: {ex}")

    finally:
        if cnxn:
            cnxn.close()

if __name__ == "__main__":
    create_database()


CACHE_MIDDLEWARE_IGNORE_PATHS = [
    
    '/builds/cart/',           # Страница корзины
    '/builds/add_to_cart/',      # Добавление в корзину
    '/builds/remove_from_cart/', # Удаление из корзины
    '/users/login/',            # Страница логина
    '/users/logout/',           # Страница выхода
    '/users/register/',         # Страница регистрации
    '/components/stock_list/',
    '/builds/checkout/',
    '/builds/employee_order_list/',
        # Добавьте это!  Убедитесь, что URL правильный
    # ... другие URL-адреса, связанные с пользователем ...
]

CACHE_MIDDLEWARE_KEY_PREFIX = 'employee_order_list_'  # Или что-то другое, уникальное