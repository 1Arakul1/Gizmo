
**Общие шаблоны:**

*   `base.html`: Базовый шаблон, который используется для всех страниц сайта. Содержит общую структуру, навигацию, подключение стилей и скриптов.

## Запуск проекта

1.  **Клонирование репозитория:**

    ```bash
    git clone <ваш_репозиторий>
    cd <название_папки_проекта>
    ```

2.  **Создание и активация виртуального окружения:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    venv\Scripts\activate  # Для Windows
    ```

3.  **Установка зависимостей:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройка базы данных:**

    *   Установите MS SQL Server и настройте подключение.
    *   Отредактируйте переменные окружения в файле `.env` (создайте его на основе примера, если его нет) и укажите параметры подключения к вашей базе данных (имя базы данных, имя пользователя, пароль, хост).  Пример содержимого `.env`:

        ```
        DJANGO_SECRET_KEY=your_secret_key
        DJANGO_DATABASE_NAME=Bony
        DJANGO_DATABASE_USER=your_db_user
        DJANGO_DATABASE_PASSWORD=your_db_password
        DJANGO_DATABASE_HOST=your_db_host
        DJANGO_DATABASE_PORT=1433  # Optional, defaults to 1433 if not specified
        ```

    *   Запустите скрипт `database_utils.py` для создания базы данных (если она еще не создана):

        ```bash
        python database_utils.py
        ```

5.  **Применение миграций:**

    ```bash
    python manage.py migrate
    ```

6.  **Создание суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```
    * (Суперпользователь также создается автоматически при первом запуске, смотрите `users/signals.py`)

7.  **Запуск сервера разработки:**

    ```bash
    python manage.py runserver
    python manage.py runserver 0.0.0.0:8000
    ```

8.  **Открытие сайта в браузере:**

    *   Перейдите по адресу `http://127.0.0.1:8000/` (или адресу, указанному в консоли при запуске сервера).

## Дополнительные настройки

*   **Настройка email:**
    *   Укажите параметры SMTP вашего почтового сервера в файле `settings.py` (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS/EMAIL_USE_SSL).
*   **Настройка кэширования:**
    *   При необходимости настройте параметры кэширования в `settings.py` (CACHES, CACHE_MIDDLEWARE_ALIAS, CACHE_MIDDLEWARE_SECONDS, CACHE_MIDDLEWARE_KEY_PREFIX).  Проверьте, что Redis сервер запущен, если вы используете Redis для кэширования.

## Используемые библиотеки

*  asgiref==3.8.1
*  Django==4.2.12
*  django-autoslug==1.9.9
*  django-mssql-backend==2.8.1
*  django-redis==5.4.0
*  django-widget-tweaks==1.5.0
*  mssql-django==1.5
*  pillow==11.1.0
*  pyodbc==5.2.0
*  python-dotenv==1.0.1
*  pytz==2025.1
*  redis==5.2.1
*  sqlparse==0.5.3
*  tzdata==2025.2

## Авторы

*   [Хакимов Нияз Фанилевич]

## Лицензия

[]

## Благодарности

[Преподователю :3]