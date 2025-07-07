# GAMES-MAIN - Дипломный проект

Проект представляет собой веб-приложение для сборки компьютеров и покупки комплектующих.

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
        DJANGO_DATABASE_NAME=Games
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

6.  **Загрузка данных из JSON файлов:**

    Прежде чем запускать сервер, необходимо загрузить данные из JSON файлов.  Убедитесь, что вы находитесь в корневой директории проекта и выполните следующие команды. Обратите внимание, что порядок загрузки важен.

    *   **Загрузка производителей (`manufacturers.json`):**

        ```bash
        python manage.py loaddata manufacturers.json
        ```

    *   **Загрузка данных комплектующих (ЦП, Материнские платы, и т.д.):**

        ```bash
        python manage.py loaddata data/initial_cpu_data.json
        python manage.py loaddata data/motherboards.json
        python manage.py loaddata data/gpus.json
        python manage.py loaddata data/rams.json
        python manage.py loaddata data/storages.json
        python manage.py loaddata data/psus.json
        python manage.py loaddata data/cases.json
        ```
        *(При необходимости, повторите для других JSON файлов с данными комплектующих.)*

7.  **Создание суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```
    * (Суперпользователь также создается автоматически при первом запуске, смотрите `users/signals.py`)

8.  **Запуск сервера разработки:**

    ```bash
    python manage.py runserver
    ```

9.  **Открытие сайта в браузере:**

    *   Перейдите по адресу `http://127.0.0.1:8000/` (или адресу, указанному в консоли при запуске сервера).

## Описание приложений

*   **builds:**  Управляет сборками компьютеров, корзиной пользователя, оформлением заказов и обработкой возвратов.  Включает модели `Build`, `CartItem`, `Order`, `OrderItem`, `ReturnRequest` и соответствующие представления для их отображения и управления.
*   **components:** Отвечает за управление компонентами компьютера, такими как CPU, GPU, Motherboard, RAM, Storage, PSU, Case и Cooler.  Определяет модели данных для каждого компонента и представления для их отображения, поиска и фильтрации. Также включает модель `Stock` для управления складскими запасами.
*   **users:**  Содержит функциональность для управления пользователями, их профилями, аутентификацией, регистрацией, сбросом пароля и управлением балансом. Включает модели `Balance` и `Transaction` для отслеживания баланса пользователей и истории транзакций.

## Описание шаблонов

*   `base.html`: Базовый шаблон, который используется для всех страниц сайта. Содержит общую структуру HTML, навигацию, подключение стилей и скриптов.

**Шаблоны приложения `builds`:**

*   `build_list.html`:  Список доступных сборок компьютеров.
*   `build_detail.html`:  Детальная информация о конкретной сборке.
*   `build_create.html`:  Форма для создания новой сборки.
*   `build_edit.html`: Форма для редактирования существующей сборки.
*   `cart.html`: Отображение корзины пользователя.
*   `checkout.html`: Страница оформления заказа.
*   `order_confirmation.html`: Страница подтверждения заказа.
*   `my_orders.html`: Список заказов текущего пользователя.
*   `employee_order_list.html`: Список текущих заказов для сотрудников (только для персонала).
*   `employee_order_update.html`: Форма обновления статуса заказа (только для персонала).
*   `employee_order_history.html`: История выданных заказов (только для персонала).
*   `employee_process_return.html`: Страница обработки запроса на возврат сотрудником.
*   `employee_return_requests.html`: Список запросов на возврат для сотрудников.
*   `stock_list.html`: Список складских запасов компонентов (только для персонала).

**Шаблоны приложения `components`:**

*   `cpu_list.html`, `gpu_list.html`, `motherboard_list.html`, `ram_list.html`, `storage_list.html`, `psu_list.html`, `case_list.html`, `cooler_list.html`: Списки соответствующих компонентов с возможностью поиска и фильтрации.
*   `cpu_detail.html`, `gpu_detail.html`, `motherboard_detail.html`, `ram_detail.html`, `storage_detail.html`, `psu_detail.html`, `case_detail.html`, `cooler_detail.html`: Детальная информация о конкретном компоненте.

**Шаблоны приложения `users`:**

*   `profile.html`: Профиль пользователя, содержащий информацию о сборках, заказах и т.д.
*   `register.html`: Форма регистрации нового пользователя.
*   `login.html`: Форма входа для существующих пользователей.
*   `password_reset.html`: Форма сброса пароля.
*   `return_request_form.html`: Форма для создания запроса на возврат.
*   `top_up_balance.html`: Форма пополнения баланса.
*   `confirm_top_up.html`: Форма подтверждения пополнения баланса.
*   `email/` : директория для хранения шаблонов писем (регистрация, сброс пароля и т.д.)
    *   `registration_email.txt`
    *   `registration_email.html`
    *   `password_reset_email.txt`
    *   `password_reset_email.html`

**Общие шаблоны:**

*   `base.html`: Базовый шаблон, который используется для всех страниц сайта. Содержит общую структуру HTML, навигацию, подключение стилей и скриптов.

## Дополнительные настройки

*   **Настройка email:**
    *   Укажите параметры SMTP вашего почтового сервера в файле `settings.py` (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS/EMAIL_USE_SSL).
*   **Настройка кэширования:**
    *   При необходимости настройте параметры кэширования в `settings.py` (CACHES, CACHE_MIDDLEWARE_ALIAS, CACHE_MIDDLEWARE_SECONDS, CACHE_MIDDLEWARE_KEY_PREFIX).  Проверьте, что Redis сервер запущен, если вы используете Redis для кэширования.

## Используемые библиотеки

*   Django
*   django-autoslug
*   django-crispy-forms
*   django-debug-toolbar
*   django-mssql-backend
*   django-redis
*   django-test-plus
*   django-widget-tweaks
*   factory_boy
*   Faker
*   flake8
*   isort
*   mypy_extensions
*   pillow
*   pyodbc
*   pytest
*   python-dotenv
*   redis

## Авторы

*   [Хакимов Нияз Фанилевич]

## Лицензия

[Укажите тип лицензии, если есть]

## Благодарности

[Преподавателю :3]
