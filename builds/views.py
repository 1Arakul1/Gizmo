# builds/views.py
import json
import logging
from decimal import Decimal
from components.models import Stock
from users.models import Balance, Transaction
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)  # Импортируем декораторы для проверки авторизации и прав пользователя
from django.contrib.sessions.models import Session  # Импортируем модель сессии
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
)  # Импортируем исключения
from django.core.mail import send_mail  # Импортируем функцию отправки email
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)  # Импортируем классы для пагинации
from django.db import transaction  # Импортируем transaction для атомарных операций с БД
from django.db.models import Q  # Импортируем Q для сложных запросов к БД
from django.http import (
    Http404,
    JsonResponse,
)  # Импортируем классы ответов
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)  # Импортируем функции для работы с запросами/ответами
from django.views.decorators.cache import (
    cache_page,
)  # Импортируем декоратор для кэширования страниц
from django.urls import reverse  # Импортируем reverse для получения URL по имени
from django.utils import timezone  # Импортируем timezone для работы с датой и временем

from django.views.decorators.http import (
    require_POST,
)  # Импортируем декоратор для обработки только POST запросов

from .forms import OrderUpdateForm  # Импортируем форму обновления заказа
from .models import (
    Build,
    CartItem,
    Order,
    OrderItem,
    ReturnRequest,
)  # Импортируем модели
from components.models import (
    CPU,
    GPU,
    Motherboard,
    RAM,
    Storage,
    PSU,
    Case,
    Cooler,
    Stock,
)  # Импортируем модели компонентов
from users.utils import (
    send_order_status_email,
)  # Импортируем утилиту для отправки email об изменении статуса заказа

logger = logging.getLogger(__name__)  # Инициализируем логгер


def employee_check(user):
    """Проверяет, является ли пользователь сотрудником (имеет ли права персонала)."""
    return user.is_staff  # Возвращает True, если пользователь является сотрудником (is_staff=True).


@user_passes_test(employee_check)
def employee_return_requests(request):
    """Отображает список запросов на возврат для сотрудников."""
    return_requests = (
        ReturnRequest.objects.all().order_by('-request_date')
    )  # Получаем все запросы на возврат, отсортированные по дате создания (от новых к старым).
    paginator = Paginator(return_requests, 10)  # Создаем объект Paginator, разбивающий запросы на страницы по 10 штук.
    page_number = request.GET.get('page')  # Получаем номер текущей страницы из GET параметра 'page'.
    try:
        page_obj = paginator.get_page(
            page_number
        )  # Получаем объект Page для текущей страницы.
    except PageNotAnInteger:
        page_obj = paginator.page(
            1
        )  # Если номер страницы не является целым числом, получаем первую страницу.
    except EmptyPage:
        page_obj = paginator.page(
            paginator.num_pages
        )  # Если номер страницы больше, чем общее количество страниц, получаем последнюю страницу.

    context = {'page_obj': page_obj}  # Создаем контекст для шаблона, передавая объект Page.
    return render(
        request, 'builds/employee_return_requests.html', context
    )  # Рендерим шаблон с запросами на возврат.


def is_employee(user):
    """Проверяет, является ли пользователь сотрудником."""
    return user.is_staff  # Возвращает True, если пользователь является сотрудником (is_staff=True).
    # Или ваша логика определения сотрудника


@login_required  # Требуется авторизация пользователя
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee)
def employee_process_return(request, return_request_id):
    """Обрабатывает запрос на возврат (сотрудник)."""
    return_request = get_object_or_404(
        ReturnRequest, pk=return_request_id
    )  # Получаем объект ReturnRequest или возвращаем 404, если не найден.
    order_item = (
        return_request.order_item
    )  # Получаем связанную позицию заказа.
    order = order_item.order  # Получаем связанный заказ.
    user = order.user  # Получаем пользователя, сделавшего заказ.

    if request.method == 'POST':  # Если это POST запрос
        status = request.POST.get('status')  # Получаем новый статус запроса из POST.
        comment = request.POST.get('comment')  # Получаем комментарий сотрудника из POST.

        try:
            with transaction.atomic():  # Оборачиваем операцию в транзакцию для атомарности.
                return_request.status = status  # Обновляем статус запроса на возврат.
                return_request.comment = comment  # Обновляем комментарий запроса на возврат.
                return_request.save()  # Сохраняем изменения в базе данных.

                if status == 'refunded':  # Если статус "Возмещены средства"
                    # Возвращаем деньги на баланс пользователя
                    balance, created = Balance.objects.get_or_create(
                        user=user
                    )  # Получаем или создаем баланс пользователя.
                    refund_amount = (
                        order_item.price * order_item.quantity
                    )  # Сумма возврата (цена товара * количество).
                    balance.balance += refund_amount  # Увеличиваем баланс пользователя.
                    balance.save()  # Сохраняем изменения в балансе.

                    # Создаем транзакцию о возврате средств
                    Transaction.objects.create(
                        user=user,
                        amount=refund_amount,
                        transaction_type='refund',
                        description=f"Возврат средств за заказ #{order.pk}, товар: {order_item.item}",
                    )  # Создаем транзакцию о возврате средств.
                    messages.success(
                        request,
                        f"Средства в размере {refund_amount} успешно возвращены пользователю {user.username}.",
                    )  # Отображаем сообщение об успехе.

                messages.success(
                    request, "Статус возврата успешно обновлен."
                )  # Отображаем сообщение об успехе.

        except Exception as e:
            messages.error(
                request, f"Ошибка при обработке возврата: {e}"
            )  # Отображаем сообщение об ошибке.

        return redirect(
            'builds:employee_order_history'
        )  # Перенаправляем на страницу истории заказов сотрудников.

    context = {
        'return_request': return_request,
        'status_choices': ReturnRequest.STATUS_CHOICES,
    }  # Создаем контекст для шаблона.
    return render(
        request, 'builds/employee_process_return.html', context
    )  # Рендерим шаблон обработки запроса на возврат.


class VaryCookieMiddleware:
    """Middleware для добавления заголовка Vary: Cookie."""

    def __init__(self, get_response):
        """Инициализация middleware."""
        self.get_response = get_response  # Сохраняем функцию получения ответа.

    def __call__(self, request):
        """Вызывается при каждом запросе."""
        response = self.get_response(request)  # Получаем ответ.
        response['Vary'] = 'Cookie'  # Добавляем заголовок Vary: Cookie.
        logger.info("VaryCookieMiddleware is running!")  # Логируем запуск middleware.
        return response  # Возвращаем ответ.


# --- Вспомогательная функция для получения cart_items и total_price (переиспользуемая) ---
def get_cart_context(request):
    """Получает контекст корзины для авторизованных пользователей."""
    cart_items = []
    total_price = Decimal('0.0')
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            try:
                item_price = item.get_total_price()
                logger.debug(f"Item: {item}, Price: {item_price}, Quantity: {item.quantity}") # LOG
                total_price += item_price
            except Exception as e:
                logger.error(f"Ошибка при обработке элемента корзины {item}: {e}")
                # Можно принять решение об исключении этого элемента из корзины или обработать как-то иначе
    return {
        'cart_items': cart_items,
        'total_price': total_price,
    }


@login_required  # Требуется авторизация пользователя
def cart_view(request):
    """Просмотр корзины."""
    logger.info(f"User in cart_view: {request.user}")  # Логируем пользователя, зашедшего в корзину.
    print(
        f"Cart items in cart_view: {CartItem.objects.filter(user=request.user)}"
    )  # Выводим в консоль элементы корзины пользователя.

    # Получаем текущую сессию, блокируя ее для обновления
    try:
        with transaction.atomic():  # Оборачиваем операцию в транзакцию для атомарности.
            Session.objects.select_for_update().get(
                session_key=request.session.session_key
            )  # Получаем сессию и блокируем ее для обновления, чтобы избежать гонок при параллельных запросах.
            cart_items = CartItem.objects.filter(
                user=request.user
            )  # Получаем элементы корзины для текущего пользователя.
            print(f"Количество элементов в корзине: {len(cart_items)}")  # Лог!
            for item in cart_items:  # Лог для каждого элемента
                print(f"Элемент корзины: {item}")
            total_price = sum(
                item.get_total_price() for item in cart_items
            )  # Суммируем стоимость товаров в корзине.
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
            }  # Создаем контекст для шаблона.
            response = render(
                request, 'builds/cart.html', context
            )  # Рендерим шаблон корзины. Сохраняем response
            response['Cache-Control'] = (
                'private, no-cache, no-store, must-revalidate'
            )  # Добавляем заголовки, запрещающие кэширование.
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response  # Возвращаем response
    except Session.DoesNotExist:
        context = {'cart_items': [], 'total_price': 0}
        return render(
            request, 'builds/cart.html', context
        )  # Если сессия не найдена, рендерим шаблон с пустой корзино


@login_required  # Требуется авторизация пользователя
@require_POST  # Требуется, чтобы запрос был методом POST
def add_to_cart(request):
    """Добавляет товар в корзину пользователя."""
    with transaction.atomic():  # Оборачиваем операцию в транзакцию для атомарности.
        logger.info(f"User in add_to_cart: {request.user}")  # Логируем пользователя, добавляющего товар в корзину.
        component_type = request.POST.get(
            'component_type'
        )  # Получаем тип товара из POST запроса.
        component_id = request.POST.get(
            'component_id'
        )  # Получаем ID товара из POST запроса.
        quantity_requested = request.POST.get(
            'quantity', '1'
        )  # Получаем запрошенное количество товара из POST запроса. Default value = 1.  Changed variable name

        logger.debug(
            f"Received data: component_type={component_type}, "
            f"component_id={component_id}, quantity={quantity_requested}"  # Changed variable name
        )  # Логируем полученные данные.

        if not component_type or not component_id:
            error_response = {
                'success': False,
                'error': 'Не указан тип или ID товара',
            }  # Создаем словарь с ответом об ошибке.
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    error_response, status=400
                )  # Если это AJAX запрос, возвращаем JSON ответ с ошибкой.
            else:
                return redirect(
                    'builds:cart'
                )  # Если это обычный запрос, перенаправляем в корзину.

        try:
            quantity_requested = int(
                quantity_requested
            )  # Преобразуем количество товара в число.  Changed variable name
            if quantity_requested < 1:  # Changed variable name
                quantity_requested = (
                    1
                )  # Если количество товара меньше 1, устанавливаем его равным 1.  Changed variable name
            component_id = int(
                component_id
            )  # Преобразуем ID товара в число.
        except ValueError:
            error_response = {
                'success': False,
                'error': 'Неверное количество',
            }  # Создаем словарь с ответом об ошибке.
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    error_response, status=400
                )  # Если это AJAX запрос, возвращаем JSON ответ с ошибкой.
            else:
                return redirect(
                    'builds:cart'
                )  # Если это обычный запрос, перенаправляем в корзину.

        component = None  # Инициализируем переменную для товара.

        if component_type == 'build':  # Если тип товара - сборка.
            try:
                component = Build.objects.get(
                    pk=component_id
                )  # Получаем сборку по ID.
                cart_item, created = CartItem.objects.get_or_create(
                    user=request.user,
                    build=component,
                    cpu=None,
                    gpu=None,
                    motherboard=None,
                    ram=None,
                    storage=None,
                    psu=None,
                    case=None,
                    cooler=None,
                )  # Получаем или создаем элемент корзины.
            except Build.DoesNotExist:
                error_response = {
                    'success': False,
                    'error': 'Сборка не найдена',
                }  # Создаем словарь с ответом об ошибке.
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse(
                        error_response, status=404
                    )  # Если это AJAX запрос, возвращаем JSON ответ с ошибкой.
                else:
                    return redirect(
                        'builds:cart'
                    )  # Если это обычный запрос, перенаправляем в корзину.

        else:  # Если тип товара - компонент.
            component_models = {
                'cpu': CPU,
                'gpu': GPU,
                'motherboard': Motherboard,
                'ram': RAM,
                'storage': Storage,
                'psu': PSU,
                'case': Case,
                'cooler': Cooler,
            }  # Словарь для сопоставления типа товара и модели.

            component_model = component_models.get(
                component_type
            )  # Получаем модель компонента по типу.

            if not component_model:
                error_response = {
                    'success': False,
                    'error': 'Неверный тип товара',
                }  # Создаем словарь с ответом об ошибке.
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse(
                        error_response, status=400
                    )  # Если это AJAX запрос, возвращаем JSON ответ с ошибкой.
                else:
                    return redirect(
                        'builds:cart'
                    )  # Если это обычный запрос, перенаправляем в корзину.

            try:
                component = component_model.objects.get(
                    pk=component_id
                )  # Получаем компонент по ID.
            except component_model.DoesNotExist:
                error_response = {
                    'success': False,
                    'error': 'Товар не найден',
                }  # Создаем словарь с ответом об ошибке.
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse(
                        error_response, status=404
                    )  # Если это AJAX запрос, возвращаем JSON ответ с ошибкой.
                else:
                    return redirect(
                        'builds:cart'
                    )  # Если это обычный запрос, перенаправляем в корзину.

            # Get stock information
            try:
                stock_item = Stock.objects.get(
                    component_type=component_type, component_id=component_id
                )  # Получаем информацию о запасах.
                available_quantity = (
                    stock_item.quantity
                )  # Получаем доступное количество товара.
            except Stock.DoesNotExist:
                available_quantity = (
                    0
                )  # Consider it out of stock if no stock entry exists.

            # Check if enough stock is available
            if (
                quantity_requested > available_quantity
            ):  # Если запрошенное количество больше доступного.
                error_message = (
                    f'На складе всего {available_quantity} единиц товара.'
                )  # Сообщение об ошибке.

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    error_response = {
                        'success': False,
                        'error': error_message,
                    }  # Создаем словарь с ответом об ошибке.
                    return JsonResponse(
                        error_response, status=400
                    )  # Если это AJAX запрос, возвращаем JSON ответ с ошибкой.
                else:
                    # Redirect back to the detail page of the component with the error message
                    # Construct the URL name dynamically
                    url_name = (
                        f'components:{component_type}_detail'
                    )  # Формируем имя URL динамически.
                    url = reverse(
                        url_name, kwargs={'pk': component_id}
                    )  # Получаем URL по имени.
                    return redirect(
                        f"{url}?error={error_message}"
                    )  # Перенаправляем на страницу товара с сообщением об ошибке.
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                build=None,
                cpu=component if component_type == 'cpu' else None,
                gpu=component if component_type == 'gpu' else None,
                motherboard=component
                if component_type == 'motherboard'
                else None,
                ram=component if component_type == 'ram' else None,
                storage=component if component_type == 'storage' else None,
                psu=component if component_type == 'psu' else None,
                case=component if component_type == 'case' else None,
                cooler=component if component_type == 'cooler' else None,
            )  # Получаем или создаем элемент корзины.
        logger.debug(
            f"CartItem created: {created}, ID: {cart_item.id}"
        )  # Логируем создание элемента корзины.

        # Обновляем количество
        if not created:  # Если элемент корзины уже существовал.
            cart_item.quantity += (
                quantity_requested
            )  # Увеличиваем количество товара в корзине.
        else:  # Если элемент корзины был создан.
            cart_item.quantity = (
                quantity_requested
            )  # Устанавливаем количество товара в корзине.

        cart_item.save()  # Сохраняем изменения в элементе корзины.

        print(
            "CartItem saved: {}, quantity: {}, component_type: {}, "
            "component_id: {}".format(
                cart_item.id,
                cart_item.quantity,
                component_type,
                component_id,
            )
        )  # Выводим в консоль информацию о сохраненном элементе корзины.
        logger.info(
            f"CartItem saved: ID={cart_item.id}, quantity={cart_item.quantity}"
        )  # Логируем сохранение элемента корзины.

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})  # Если это AJAX запрос, возвращаем JSON ответ об успехе.
        else:
            return redirect(
                'builds:cart'
            )  # Redirect to cart on success. Если это обычный запрос, перенаправляем в корзину.


@login_required  # Требуется авторизация пользователя
def remove_from_cart(request, item_id):
    """Удаление товара из корзины."""
    try:
        cart_item = get_object_or_404(
            CartItem, pk=item_id, user=request.user
        )  # Получаем элемент корзины или возвращаем 404, если не найден.
        cart_item.delete()  # Удаляем элемент корзины.
        messages.success(
            request, "Товар успешно удален из корзины."
        )  # Отображаем сообщение об успехе.
    except Http404:
        messages.error(
            request, "Товар не найден в корзине."
        )  # Отображаем сообщение об ошибке.
    return redirect(
        'builds:cart'
    )  # Перенаправляем в корзину.


def build_list(request):
    """Отображает список сборок."""
    builds_list = Build.objects.all().order_by('id')  # Получаем все сборки, отсортированные по ID.
    paginator = Paginator(builds_list, 6)  # Создаем объект Paginator, разбивающий сборки на страницы по 6 штук.
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET параметра 'page'.

    try:
        builds = paginator.page(
            page
        )  # Получаем объект Page для текущей страницы.
    except PageNotAnInteger:
        builds = paginator.page(
            1
        )  # Если номер страницы не является целым числом, получаем первую страницу.
    except EmptyPage:
        builds = paginator.page(
            paginator.num_pages
        )  # Если номер страницы больше, чем общее количество страниц, получаем последнюю страницу.

    # --- Получаем контекст корзины ---
    cart_context = get_cart_context(
        request
    )  # Получаем контекст корзины для отображения в шаблоне.
    # --- Добавляем в контекст шаблона ---
    context = {
        'builds': builds,
        **cart_context,  # Распаковываем cart_context (cart_items, total_price)
    }  # Создаем контекст для шаблона.
    return render(
        request, 'builds/build_list.html', context
    )  # Рендерим шаблон списка сборок.


def build_detail(request, pk):
    """Отображает детальную информацию о сборке."""
    build = get_object_or_404(
        Build, pk=pk
    )  # Получаем сборку по ID или возвращаем 404, если не найдена.
    cart_context = get_cart_context(
        request
    )  # добавляем корзину в контекст
    context = {
        'build': build,
        **cart_context,  # Распаковываем cart_context (cart_items, total_price)
    }  # Создаем контекст для шаблона.
    return render(
        request, 'builds/build_detail.html', context
    )  # Рендерим шаблон детальной информации о сборке.


def build_create(request):
    """Создает новую сборку."""
    if request.method == 'POST':  # Если это POST запрос.
        # Получаем данные из POST
        cpu_id = request.POST.get('cpu')
        gpu_id = request.POST.get('gpu')
        motherboard_id = request.POST.get('motherboard')
        ram_id = request.POST.get('ram')
        storage_id = request.POST.get('storage')
        psu_id = request.POST.get('psu')
        case_id = request.POST.get('case')
        cooler_id = request.POST.get('cooler')

        # Функция для проверки наличия и получения компонента
        def get_component_if_in_stock(model, component_id):
            """
            Проверяет, есть ли компонент в наличии на складе, и возвращает его, если есть.

            Args:
                model: Модель компонента (CPU, GPU, Motherboard и т.д.).
                component_id: ID компонента.

            Returns:
                Объект компонента, если он есть в наличии, иначе None.
            """
            if not component_id:
                return None
            try:
                component = get_object_or_404(
                    model, pk=component_id
                )  # Получаем компонент по ID.
                # Проверяем наличие через Stock
                try:
                    stock = Stock.objects.get(
                        component_type=model._meta.model_name,
                        component_id=component_id,
                    )  # Получаем информацию о запасах.
                    if (
                        stock.quantity > 0
                    ):  # Если количество товара на складе больше 0.
                        return component  # Возвращаем компонент.
                    else:
                        return (
                            None
                        )  # Товар не в наличии, возвращаем None.
                except Stock.DoesNotExist:
                    return (
                        None
                    )  # Stock object doesn't exist, returning None
            except (ValueError, TypeError, ObjectDoesNotExist):
                return (
                    None
                )  # Если произошла ошибка, возвращаем None.

        # Получаем объекты компонентов с проверкой наличия
        cpu = get_component_if_in_stock(CPU, cpu_id)
        gpu = get_component_if_in_stock(GPU, gpu_id)
        motherboard = get_component_if_in_stock(Motherboard, motherboard_id)
        ram = get_component_if_in_stock(RAM, ram_id)
        storage = get_component_if_in_stock(Storage, storage_id)
        psu = get_component_if_in_stock(PSU, psu_id)
        case = get_component_if_in_stock(Case, case_id)
        cooler = get_component_if_in_stock(Cooler, cooler_id)

        # Проверяем, что все компоненты в наличии
        missing_components = []  # Создаем список отсутствующих компонентов.
        if cpu_id and not cpu:
            missing_components.append('Процессор')
        if gpu_id and not gpu:
            missing_components.append('Видеокарта')
        if motherboard_id and not motherboard:
            missing_components.append('Материнская плата')
        if ram_id and not ram:
            missing_components.append('Оперативная память')
        if storage_id and not storage:
            missing_components.append('Накопитель')
        if psu_id and not psu:
            missing_components.append('Блок питания')
        if case_id and not case:
            missing_components.append('Корпус')
        if cooler_id and not cooler:
            missing_components.append('Охлаждение')

        if missing_components:  # Если есть отсутствующие компоненты.
            return render(
                request,
                'builds/build_create.html',
                {
                    'error_message': f'Следующие компоненты отсутствуют на складе: {", ".join(missing_components)}',
                    'cpus': CPU.objects.all(),
                    'gpus': GPU.objects.all(),
                    'motherboards': Motherboard.objects.all(),
                    'rams': RAM.objects.all(),
                    'storages': Storage.objects.all(),
                    'psus': PSU.objects.all(),
                    'cases': Case.objects.all(),
                    'coolers': Cooler.objects.all(),
                },
            )  # Отображаем страницу создания сборки с сообщением об ошибке.

        # Проверки совместимости
        error_message = None  # Инициализируем переменную для сообщения об ошибке совместимости.

        if cpu and motherboard:
            if not cpu.is_compatible_with_motherboard(
                motherboard
            ):  # Проверяем совместимость процессора и материнской платы.
                error_message = (
                    'Процессор не совместим с материнской платой.'
                )  # Сообщение об ошибке.

        if motherboard and ram:
            if not motherboard.is_compatible_with_ram(
                ram
            ):  # Проверяем совместимость материнской платы и оперативной памяти.
                error_message = (
                    'Оперативная память не совместима с материнской платой.'
                )  # Сообщение об ошибке.

        if gpu and psu:
            if not psu.is_sufficient_for_gpu(
                gpu
            ):  # Проверяем достаточно ли мощности блока питания для видеокарты.
                error_message = (
                    'Мощности блока питания недостаточно для видеокарты.'
                )  # Сообщение об ошибке.

        if cpu and cooler:
            if not cooler.is_compatible_with_cpu(
                cpu
            ):  # Проверяем совместимость кулера и процессора.
                error_message = 'Кулер не совместим с процессором.'  # Сообщение об ошибке.

        if error_message:  # Если есть ошибка совместимости.
            return render(
                request,
                'builds/build_create.html',
                {
                    'error_message': error_message,
                    'cpus': CPU.objects.all(),
                    'gpus': GPU.objects.all(),
                    'motherboards': Motherboard.objects.all(),
                    'rams': RAM.objects.all(),
                    'storages': Storage.objects.all(),
                    'psus': PSU.objects.all(),
                    'cases': Case.objects.all(),
                    'coolers': Cooler.objects.all(),
                },
            )  # Отображаем страницу создания сборки с сообщением об ошибке.

        # Создаем сборку
        total_price = sum(
            component.price
            for component in [cpu, gpu, motherboard, ram, storage, psu, case, cooler]
            if component and component.price is not None
        )  # Вычисляем общую стоимость сборки.

        build = Build(
            user=request.user,
            cpu=cpu,
            gpu=gpu,
            motherboard=motherboard,
            ram=ram,
            storage=storage,
            psu=psu,
            case=case,
            cooler=cooler,
        )  # Создаем объект сборки.

        try:
            build.save()  # Сохраняем сборку в базе данных.
            return redirect(
                'builds:build_detail', pk=build.pk
            )  # Перенаправляем на страницу детальной информации о сборке.
        except ValidationError as e:
            return render(
                request,
                'builds/build_create.html',
                {
                    'error_message': f'Ошибка сохранения сборки: {e}',
                    'cpus': CPU.objects.all(),
                    'gpus': GPU.objects.all(),
                    'motherboards': Motherboard.objects.all(),
                    'rams': RAM.objects.all(),
                    'storages': Storage.objects.all(),
                    'psus': PSU.objects.all(),
                    'cases': Case.objects.all(),
                    'coolers': Cooler.objects.all(),
                },
            )  # Отображаем страницу создания сборки с сообщением об ошибке.
    else:  # Если это GET запрос.
        # Get components that are in stock
        def get_in_stock_components(model):
            """Получает компоненты, которые есть в наличии на складе."""
            model_name = model._meta.model_name  # Получаем имя модели.
            in_stock_ids = Stock.objects.filter(
                component_type=model_name, quantity__gt=0
            ).values_list(
                'component_id', flat=True
            )  # Получаем ID компонентов, которые есть в наличии.
            return model.objects.filter(
                id__in=in_stock_ids
            )  # Возвращаем компоненты, которые есть в наличии.

        cpus = get_in_stock_components(CPU)
        gpus = get_in_stock_components(GPU)
        motherboards = get_in_stock_components(Motherboard)
        rams = get_in_stock_components(RAM)
        storages = get_in_stock_components(Storage)
        psus = get_in_stock_components(PSU)
        cases = get_in_stock_components(Case)
        coolers = get_in_stock_components(Cooler)

        context = {
            'cpus': cpus,
            'gpus': gpus,
            'motherboards': motherboards,
            'rams': rams,
            'storages': storages,
            'psus': psus,
                        'cases': cases,
            'coolers': coolers,
        }  # Создаем контекст для шаблона.
        return render(
            request, 'builds/build_create.html', context
        )  # Отображаем страницу создания сборки с компонентами в наличии.


def build_preview(request):
    """Предпросмотр сборки."""
    if request.method == 'POST':  # Если это POST запрос.
        try:
            data = json.loads(
                request.body
            )  # Пытаемся распарсить JSON данные из тела запроса.
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Неверный формат данных'}, status=400
            )  # Если не удалось распарсить JSON, возвращаем ошибку.

        cpu_id = data.get('cpu')  # Получаем ID процессора из данных.
        gpu_id = data.get('gpu')  # Получаем ID видеокарты из данных.
        motherboard_id = data.get('motherboard')  # Получаем ID материнской платы из данных.
        ram_id = data.get('ram')  # Получаем ID оперативной памяти из данных.
        storage_id = data.get('storage')  # Получаем ID накопителя из данных.
        psu_id = data.get('psu')  # Получаем ID блока питания из данных.
        case_id = data.get('case')  # Получаем ID корпуса из данных.
        cooler_id = data.get('cooler')  # Получаем ID кулера из данных.

        try:
            cpu = CPU.objects.get(pk=cpu_id) if cpu_id else None  # Получаем процессор по ID.
            gpu = GPU.objects.get(pk=gpu_id) if gpu_id else None  # Получаем видеокарту по ID.
            motherboard = (
                Motherboard.objects.get(pk=motherboard_id)
                if motherboard_id
                else None
            )  # Получаем материнскую плату по ID.
            ram = RAM.objects.get(pk=ram_id) if ram_id else None  # Получаем оперативную память по ID.
            storage = (
                Storage.objects.get(pk=storage_id) if storage_id else None
            )  # Получаем накопитель по ID.
            psu = PSU.objects.get(pk=psu_id) if psu_id else None  # Получаем блок питания по ID.
            case = Case.objects.get(pk=case_id) if case_id else None  # Получаем корпус по ID.
            cooler = (
                Cooler.objects.get(pk=cooler_id) if cooler_id else None
            )  # Получаем кулер по ID.
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': 'Один из компонентов не найден'}, status=400
            )  # Если один из компонентов не найден, возвращаем ошибку.

        error_message = None  # Инициализируем переменную для сообщения об ошибке совместимости.

        if (
            cpu
            and motherboard
            and not cpu.is_compatible_with_motherboard(motherboard)
        ):  # Проверяем совместимость процессора и материнской платы.
            error_message = (
                'Процессор не совместим с материнской платой.'
            )  # Сообщение об ошибке.

        if (
            motherboard
            and ram
            and not motherboard.is_compatible_with_ram(ram)
        ):  # Проверяем совместимость материнской платы и оперативной памяти.
            error_message = (
                'Оперативная память не совместима с материнской платой.'
            )  # Сообщение об ошибке.

        if gpu and psu and not psu.is_sufficient_for_gpu(gpu):
            error_message = (
                'Мощности блока питания недостаточно для видеокарты.'
            )  # Сообщение об ошибке.

        if cpu and cooler and not cooler.is_compatible_with_cpu(cpu):
            error_message = 'Кулер не совместим с процессором.'  # Сообщение об ошибке.

        total_price = sum(
            c.price
            for c in [cpu, gpu, motherboard, ram, storage, psu, case, cooler]
            if c and c.price is not None
        )  # Вычисляем общую стоимость сборки.

        context = {
            'cpu': cpu,
            'gpu': gpu,
            'motherboard': motherboard,
            'ram': ram,
            'storage': storage,
            'psu': psu,
            'case': case,
            'cooler': cooler,
            'total_price': total_price,
            'error_message': error_message,
        }  # Создаем контекст для шаблона.
        html = (
            render(request, 'builds/build_preview.html', context)
            .content.decode('utf-8')
        )  # Рендерим шаблон предпросмотра сборки и декодируем его в строку.

        return JsonResponse(
            {'html': html}
        )  # Возвращаем JSON ответ с HTML кодом предпросмотра.

    return JsonResponse(
        {'html': ''}
    )  # Если это не POST запрос, возвращаем пустой HTML.


def build_edit(request, pk):
    """Редактирует существующую сборку."""
    build = get_object_or_404(
        Build, pk=pk
    )  # Получаем сборку по ID или возвращаем 404, если не найдена.

    if request.method == 'POST':  # Если это POST запрос.
        # Получаем данные из POST
        cpu_id = request.POST.get('cpu')
        gpu_id = request.POST.get('gpu')
        motherboard_id = request.POST.get('motherboard')
        ram_id = request.POST.get('ram')
        storage_id = request.POST.get('storage')
        psu_id = request.POST.get('psu')
        case_id = request.POST.get('case')
        cooler_id = request.POST.get('cooler')

        # Получаем объекты компонентов, обрабатывая ошибки
        try:
            cpu = CPU.objects.get(pk=cpu_id) if cpu_id else None  # Получаем процессор по ID.
            gpu = GPU.objects.get(pk=gpu_id) if gpu_id else None  # Получаем видеокарту по ID.
            motherboard = (
                Motherboard.objects.get(pk=motherboard_id)
                if motherboard_id
                else None
            )  # Получаем материнскую плату по ID.
            ram = RAM.objects.get(pk=ram_id) if ram_id else None  # Получаем оперативную память по ID.
            storage = (
                Storage.objects.get(pk=storage_id) if storage_id else None
            )  # Получаем накопитель по ID.
            psu = PSU.objects.get(pk=psu_id) if psu_id else None  # Получаем блок питания по ID.
            case = Case.objects.get(pk=case_id) if case_id else None  # Получаем корпус по ID.
            cooler = (
                Cooler.objects.get(pk=cooler_id) if cooler_id else None
            )  # Получаем кулер по ID.
        except (
            CPU.DoesNotExist,
            GPU.DoesNotExist,
            Motherboard.DoesNotExist,
            RAM.DoesNotExist,
            Storage.DoesNotExist,
            PSU.DoesNotExist,
            Case.DoesNotExist,
            Cooler.DoesNotExist,
        ):  # Обрабатываем исключения, если компонент не найден.
            return render(
                request,
                'builds/build_edit.html',
                {
                    'build': build,
                    'error_message': 'Один из выбранных компонентов не найден.',
                    'cpus': CPU.objects.all(),
                    'gpus': GPU.objects.all(),
                    'motherboards': Motherboard.objects.all(),
                    'rams': RAM.objects.all(),
                    'storages': Storage.objects.all(),
                    'psus': PSU.objects.all(),
                    'cases': Case.objects.all(),
                    'coolers': Cooler.objects.all(),  # Добавляем coolers
                },
            )  # Отображаем страницу редактирования сборки с сообщением об ошибке.
        error_message = None  # Инициализируем переменную для сообщения об ошибке совместимости.

        if cpu and motherboard:
            if not cpu.is_compatible_with_motherboard(
                motherboard
            ):  # Проверяем совместимость процессора и материнской платы.
                error_message = (
                    'Процессор не совместим с материнской платой.'
                )  # Сообщение об ошибке.

        if motherboard and ram:
            if not motherboard.is_compatible_with_ram(
                ram
            ):  # Проверяем совместимость материнской платы и оперативной памяти.
                error_message = (
                    'Оперативная память не совместима с материнской платой.'
                )  # Сообщение об ошибке.

        if gpu and psu:
            if not psu.is_sufficient_for_gpu(
                gpu
            ):  # Проверяем достаточно ли мощности блока питания для видеокарты.
                error_message = (
                    'Мощности блока питания недостаточно для видеокарты.'
                )  # Сообщение об ошибке.

        if cpu and cooler:
            if not cooler.is_compatible_with_cpu(
                cpu
            ):  # Проверяем совместимость кулера и процессора.
                error_message = 'Кулер не совместим с процессором.'  # Сообщение об ошибке.

        if error_message:  # Если есть ошибка совместимости.
            return render(
                request,
                'builds/build_edit.html',
                {
                    'build': build,
                    'error_message': error_message,
                    'cpus': CPU.objects.all(),
                    'gpus': GPU.objects.all(),
                    'motherboards': Motherboard.objects.all(),
                    'rams': RAM.objects.all(),
                    'storages': Storage.objects.all(),
                    'psus': PSU.objects.all(),
                    'cases': Case.objects.all(),
                    'coolers': Cooler.objects.all(),  # Добавляем coolers
                },
            )  # Отображаем страницу редактирования сборки с сообщением об ошибке.

        #  Обновление полей build
        build.cpu = cpu  # Обновляем процессор.
        build.gpu = gpu  # Обновляем видеокарту.
        build.motherboard = motherboard  # Обновляем материнскую плату.
        build.ram = ram  # Обновляем оперативную память.
        build.storage = storage  # Обновляем накопитель.
        build.psu = psu  # Обновляем блок питания.
        build.case = case  # Обновляем корпус.
        build.cooler = cooler  # Добавлено обновление кулера

        # Рассчитываем общую стоимость
        total_price = Decimal('0.0')  # Инициализируем общую стоимость.
        if build.cpu:
            total_price += build.cpu.price  # Добавляем цену процессора.
        if build.gpu:
            total_price += build.gpu.price  # Добавляем цену видеокарты.
        if build.motherboard:
            total_price += build.motherboard.price  # Добавляем цену материнской платы.
        if build.ram:
            total_price += build.ram.price  # Добавляем цену оперативной памяти.
        if build.storage:
            total_price += build.storage.price  # Добавляем цену накопителя.
        if psu:
            total_price += build.psu.price  # Добавляем цену блока питания.
        if case:
            total_price += build.case.price  # Добавляем цену корпуса.
        if cooler:
            total_price += build.cooler.price  # Добавляем цену кулера
        build.total_price = total_price  # Обновляем общую стоимость сборки.

        try:
            build.save()  # Сохраняем сборку в базе данных.
            return redirect(
                'builds:build_detail', pk=build.pk
            )  # Перенаправляем на страницу детальной информации о сборке.
        except ValidationError as e:  # Обрабатываем исключение, если возникла ошибка валидации.
            return render(
                request,
                'builds/build_edit.html',
                {
                    'build': build,
                    'error_message': f'Ошибка сохранения сборки: {e}',
                    'cpus': CPU.objects.all(),
                    'gpus': GPU.objects.all(),
                    'motherboards': Motherboard.objects.all(),
                    'rams': RAM.objects.all(),
                    'storages': Storage.objects.all(),
                    'psus': PSU.objects.all(),
                    'cases': Case.objects.all(),
                    'coolers': Cooler.objects.all(),  # Добавляем coolers
                },
            )  # Отображаем страницу редактирования сборки с сообщением об ошибке.

    else:  # Если это GET запрос.
        # Отобразите форму с текущими значениями
        cpus = CPU.objects.all()  # Получаем все процессоры.
        gpus = GPU.objects.all()  # Получаем все видеокарты.
        motherboards = Motherboard.objects.all()  # Получаем все материнские платы.
        rams = RAM.objects.all()  # Получаем всю оперативную память.
        storages = Storage.objects.all()  # Получаем все накопители.
        psus = PSU.objects.all()  # Получаем все блоки питания.
        cases = Case.objects.all()  # Получаем все корпуса.
        coolers = Cooler.objects.all()  # Получаем все кулеры.

        context = {
            'build': build,
            'cpus': cpus,
            'gpus': gpus,
            'motherboards': motherboards,
            'rams': rams,
            'storages': storages,
            'psus': psus,
            'cases': cases,
            'coolers': coolers,
        }  # Создаем контекст для шаблона.
        return render(
            request, 'builds/build_edit.html', context
        )  # Отображаем страницу редактирования сборки с текущими значениями.


# Форма
class CustomOrderUpdateForm(OrderUpdateForm):
    """Кастомная форма обновления заказа, позволяющая передавать choices для поля status."""

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму.

        Args:
            *args: Аргументы для родительского класса.
            **kwargs: Ключевые аргументы для родительского класса. Должен содержать status_choices.
        """
        status_choices = kwargs.pop(
            'status_choices', []
        )  # Извлекаем status_choices из kwargs, если есть.
        super().__init__(*args, **kwargs)  # Вызываем конструктор родительского класса.
        self.fields[
            'status'
        ].choices = (
            status_choices
        )  # Задаём в конструкторе варианты выбора для поля status.


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee).
def employee_order_list(request):
    """Отображает список заказов для сотрудников."""
    logger.info(
        f"employee_order_list GET parameters: {request.GET}"
    )  # Логируем параметры GET запроса.
    logger.info(
        f"User is authenticated: {request.user.is_authenticated}"
    )  # Логируем, авторизован ли пользователь.
    logger.info(
        f"User is employee: {is_employee(request.user)}"
    )  # Логируем, является ли пользователь сотрудником.

    query = request.GET.get('q')  # Получаем поисковой запрос из GET параметров.
    # refresh = request.GET.get('refresh')  # Больше не нужен

    if query:  # Если есть поисковой запрос.
        orders = Order.objects.filter(
            Q(is_completed=False)
            & (
                Q(track_number__icontains=query)
                | Q(user__username__icontains=query)
                | Q(email__icontains=query)
            )
        ).order_by(
            '-order_date'
        )  # Фильтруем заказы по поисковому запросу и сортируем по дате (от новых к старым).
    else:  # Если нет поискового запроса.
        orders = Order.objects.filter(
            is_completed=False
        ).order_by(
            '-order_date'
        )  # Получаем все незавершенные заказы и сортируем по дате (от новых к старым).

    # Пагинация
    paginator = Paginator(
        orders, 10
    )  # Создаем объект Paginator, разбивающий заказы на страницы по 10 штук.
    page_number = request.GET.get('page')  # Получаем номер текущей страницы.
    try:
        page_obj = paginator.get_page(
            page_number
        )  # Получаем объект Page для текущей страницы.
    except PageNotAnInteger:
        page_obj = paginator.page(
            1
        )  # Если номер страницы не является целым числом, получаем первую страницу.
    except EmptyPage:
        page_obj = paginator.page(
            paginator.num_pages
        )  # Если номер страницы больше, чем общее количество страниц, получаем последнюю страницу.

    # Получаем количество запросов на возврат
    return_request_count = ReturnRequest.objects.filter(
        status='pending'
    ).count()  # Получаем количество запросов на возврат со статусом "pending".

    # Получаем количество товаров, отсутствующих на складе
    out_of_stock_count = request.GET.get(
        'out_of_stock_count', Stock.objects.filter(quantity=0).count()
    )  # Получаем количество товаров, которых нет в наличии.

    return render(
        request,
        'builds/employee_order_list.html',
        {
            'page_obj': page_obj,
            'query': query,
            'return_request_count': return_request_count,
            'out_of_stock_count': out_of_stock_count,
        },  # Добавляем return_request_count
    )  # Отображаем страницу со списком заказов.


# Представление для обновления статуса заказа
@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee).
def employee_order_update(request, order_id):
    """Обновляет статус заказа."""
    try:
        order = Order.objects.get(
            pk=order_id
        )  # Получаем заказ по ID. Если не найден, вызывается исключение.
    except Order.DoesNotExist:
        raise Http404(
            "Order not found"
        )  # Если заказ не найден, возвращаем 404.

    # Определение доступных статусов на основе доставки
    if order.delivery_option == 'courier':  # Если выбрана курьерская доставка
        status_choices = [
            ('pending', 'Заказ на рассмотрении'),
            ('confirmed', 'Заказ подтверждён'),
            ('assembling', 'Заказ собирается'),
            ('delivery_prep', 'Заказ готовится к доставке'),
            (
                'delivering',
                'Заказ будет доставлен вам в течении 3 часов',
            ),
            ('completed', 'Заказ выполнен'),
        ]  # Возможные статусы для курьерской доставки
    else:  # Самовывоз или другой способ доставки
        status_choices = [
            ('pending', 'Заказ на рассмотрении'),
            ('confirmed', 'Заказ подтверждён'),
            ('delivered', 'Заказ доставлен, заберите его'),
            ('completed', 'Заказ выполнен'),
        ]  # Возможные статусы для самовывоза.

    if request.method == 'POST':  # Если это POST запрос
        form = CustomOrderUpdateForm(
            request.POST, instance=order, status_choices=status_choices
        )  # Создаем форму с данными из POST запроса и передаем возможные статусы.
        if form.is_valid():  # Если форма валидна
            old_status = order.status  # Сохраняем старый статус для сравнения
            form.save()  # Сохраняем изменения в заказе
            new_status = order.status  # Получаем новый статус заказа

            # Отправка email уведомления, если статус изменился
            if new_status in [
                'delivered',
                'delivering',
            ] and old_status != new_status:  # Если статус стал "доставлен" или "в доставке" и изменился
                send_order_status_email(
                    order
                )  # Отправляем уведомление по электронной почте

            messages.success(
                request, f"Статус заказа #{order.pk} успешно изменен."
            )  # Отображаем сообщение об успехе.
            return redirect(
                'builds:employee_order_list'
            )  # Перенаправляем на страницу списка заказов.
    else:  # Если это GET запрос
        form = CustomOrderUpdateForm(
            instance=order, status_choices=status_choices
        )  # Создаем форму с текущими данными заказа и передаем возможные статусы.

    return render(
        request,
        'builds/employee_order_update.html',
        {'form': form, 'order': order},
    )  # Отображаем страницу обновления статуса заказа.


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee).
def employee_order_complete(request, order_id):
    """Отмечает заказ как выполненный (выданный)."""
    order = get_object_or_404(
        Order, pk=order_id
    )  # Получаем заказ по ID или возвращаем 404, если не найден.
    order.is_completed = (
        True  # Устанавливаем флаг is_completed в True (заказ выдан).
    )
    order.status = 'completed'  # Устанавливаем статус заказа в "completed".
    order.save()  # Сохраняем изменения в заказе.

    logger.info(
        f"Order {order.pk} status after update: {order.status}, "
        f"is_completed: {order.is_completed}"
    )  # Логируем изменение статуса заказа.

    messages.success(
        request, f"Заказ #{order.pk} отмечен как выданный."
    )  # Отображаем сообщение об успехе.
    return redirect(
        'builds:employee_order_list'
    )  # Перенаправляем на страницу списка заказов.


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee).
def employee_order_history(request):
    """Отображает историю выданных заказов с информацией о возвратах."""
    query = request.GET.get('q')  # Получаем поисковой запрос из GET параметров.
    if query:  # Если есть поисковой запрос.
        orders = (
            Order.objects.filter(
                Q(is_completed=True)
                & (
                    Q(track_number__icontains=query)
                    | Q(user__username__icontains=query)
                    | Q(email__icontains=query)
                )
            )
            .order_by('-order_date')
            .prefetch_related(
                'return_request'
            )  # Оптимизация запроса - предварительная загрузка связанных запросов на возврат.
        )  # Фильтруем завершенные заказы по поисковому запросу и сортируем по дате (от новых к старым).
    else:  # Если нет поискового запроса.
        orders = (
            Order.objects.filter(is_completed=True)
            .order_by('-order_date')
            .prefetch_related(
                'return_request'
            )  # Оптимизация запроса - предварительная загрузка связанных запросов на возврат.
        )  # Получаем все завершенные заказы и сортируем по дате (от новых к старым).

    # Пагинация
    paginator = Paginator(
        orders, 10
    )  # По 10 заказов на страницу # Создаем объект Paginator, разбивающий заказы на страницы по 10 штук.
    page_number = request.GET.get('page')  # Получаем номер текущей страницы.
    try:
        page_obj = paginator.get_page(
            page_number
        )  # Получаем объект Page для текущей страницы.
    except PageNotAnInteger:
        page_obj = paginator.page(
            1
        )  # Если номер страницы не является целым числом, получаем первую страницу.
    except EmptyPage:
        page_obj = paginator.page(
            paginator.num_pages
        )  # Если номер страницы больше, чем общее количество страниц, получаем последнюю страницу.

    context = {'page_obj': page_obj, 'query': query}  # Создаем контекст для шаблона.
    return render(
        request, 'builds/employee_order_history.html', context
    )  # Отображаем страницу с историей заказов.


@login_required  # Требуется авторизация пользователя.
def checkout(request):
    """Обрабатывает оформление заказа."""
    cart_items = CartItem.objects.filter(
        user=request.user
    )  # Получаем все элементы корзины для текущего пользователя.
    total_price = sum(
        item.get_total_price() for item in cart_items
    )  # Вычисляем общую стоимость товаров в корзине.
    user = request.user  # Получаем текущего пользователя

    if request.method == 'POST':  # Если это POST запрос
        email = request.POST.get('email')  # Получаем email из POST запроса.
        delivery_option = request.POST.get(
            'delivery_option'
        )  # Получаем способ доставки из POST запроса.
        payment_method = request.POST.get(
            'payment_method'
        )  # Получаем способ оплаты из POST запроса.
        address = request.POST.get('address')  # Получаем адрес доставки из POST запроса.

        if (
            not email or not delivery_option or not payment_method
        ):  # Если какое-либо поле не заполнено.
            messages.error(request, "Пожалуйста, заполните все поля.")  # Выводим сообщение об ошибке.
            return render(
                request,
                'builds/checkout.html',
                {'cart_items': cart_items, 'total_price': total_price},
            )  # Отображаем страницу оформления заказа с сообщением об ошибке.

        try:
            with transaction.atomic():  # Оборачиваем операцию в транзакцию для атомарности.
                # Создание заказа (определяем order до if payment_method == 'balance')
                order = Order.objects.create(
                    user=user,
                    email=email,
                    delivery_option=delivery_option,
                    payment_method=payment_method,
                    address=address,
                    total_amount=total_price,
                    order_date=timezone.now(),
                )  # Создаем объект заказа.

                # Проверяем, выбран ли способ оплаты "С личного счета"
                if (
                    payment_method == 'balance'
                ):  # Если выбран способ оплаты "С личного счета".
                    # Получаем баланс пользователя
                    balance, created = Balance.objects.get_or_create(
                        user=user
                    )  # Получаем или создаем баланс пользователя.

                    # Проверяем, достаточно ли средств на балансе
                    if (
                        balance.balance < total_price
                    ):  # Если на балансе недостаточно средств.
                        messages.error(
                            request,
                            "Недостаточно средств на балансе. Пополните счет.",
                        )  # Выводим сообщение об ошибке.
                        return render(
                            request,
                            'builds/checkout.html',
                            {'cart_items': cart_items, 'total_price': total_price},
                        )  # Отображаем страницу оформления заказа с сообщением об ошибке.

                    # Списываем средства с баланса
                    balance.balance -= total_price  # Списываем средства с баланса пользователя.
                    balance.save()  # Сохраняем изменения в балансе.

                    # Создаем транзакцию о списании средств
                    Transaction.objects.create(
                        user=user,
                        amount=total_price,
                        transaction_type='purchase',
                        description=f"Оплата заказа #{order.pk}",  # Номер заказа будет известен после создания
                    )  # Создаем транзакцию о списании средств.

                # Создание позиций заказа
                for item in cart_items:  # Для каждого элемента в корзине.
                    component_type = None  # Инициализируем тип компонента.
                    component_id = None  # Инициализируем ID компонента.

                    if item.build:  # Если это сборка.
                        component_type = 'build'  # Устанавливаем тип компонента в "build".
                        component_id = item.build.pk  # Получаем ID сборки.
                    elif item.cpu:  # Если это процессор.
                        component_type = 'cpu'  # Устанавливаем тип компонента в "cpu".
                        component_id = item.cpu.pk  # Получаем ID процессора.
                    elif item.gpu:  # Если это видеокарта.
                        component_type = 'gpu'  # Устанавливаем тип компонента в "gpu".
                        component_id = item.gpu.pk  # Получаем ID видеокарты.
                    elif item.motherboard:  # Если это материнская плата.
                        component_type = (
                            'motherboard'  # Устанавливаем тип компонента в "motherboard".
                        )
                        component_id = (
                            item.motherboard.pk
                        )  # Получаем ID материнской платы.
                    elif item.ram:  # Если это оперативная память.
                        component_type = 'ram'  # Устанавливаем тип компонента в "ram".
                        component_id = (
                            item.ram.pk
                        )  # Получаем ID оперативной памяти.
                    elif item.storage:  # Если это накопитель.
                        component_type = (
                            'storage'  # Устанавливаем тип компонента в "storage".
                        )
                        component_id = (
                            item.storage.pk
                        )  # Получаем ID накопителя.
                    elif item.psu:  # Если это блок питания.
                        component_type = 'psu'  # Устанавливаем тип компонента в "psu".
                        component_id = (
                            item.psu.pk
                        )  # Получаем ID блока питания.
                    elif item.case:  # Если это корпус.
                        component_type = 'case'  # Устанавливаем тип компонента в "case".
                        component_id = item.case.pk  # Получаем ID корпуса.
                    elif item.cooler:  # Если это кулер.
                        component_type = 'cooler'  # Устанавливаем тип компонента в "cooler".
                        component_id = item.cooler.pk  # Получаем ID кулера.

                    OrderItem.objects.create(
                        order=order,
                        item=str(item),  # Преобразуем товар в строку
                        quantity=item.quantity,
                        price=item.get_total_price() / item.quantity,
                        component_type=component_type,
                        component_id=component_id,
                    )  # Создаем позицию заказа.

                # Очистка корзины после оформления заказа
                cart_items.delete()  # Удаляем все элементы из корзины.

                # Отправка уведомления по электронной почте
                subject = 'Ваш заказ оформлен!'  # Тема письма.
                message = (
                    f'Спасибо за ваш заказ! \n\nСумма заказа: {total_price} ₽\n'
                    f'Способ доставки: {order.delivery_option}\n'
                    f'Способ оплаты: {order.payment_method}\n'
                    f'Адрес доставки: {order.address}\n'
                    f'Ваш трек-номер: {order.track_number}'
                )  # Тело письма.
                from_email = settings.EMAIL_HOST_USER  # Email отправителя.
                recipient_list = [email]  # Email получателя.

                try:
                    send_mail(
                        subject, message, from_email, recipient_list
                    )  # Отправляем письмо.
                    success = True  # Устанавливаем флаг успеха.
                except Exception as e:  # Если произошла ошибка при отправке письма.
                    messages.error(
                        request,
                        f"Заказ оформлен, но не удалось отправить уведомление: {e}",
                    )  # Выводим сообщение об ошибке.
                    success = False  # Устанавливаем флаг неудачи.

                # Перенаправление на страницу подтверждения с параметром в URL
                if success:  # Если заказ успешно оформлен.
                    return redirect(
                        reverse('builds:order_confirmation')
                        + f'?success=True&track_number={order.track_number}'
                    )  # Перенаправляем на страницу подтверждения с параметром success=True.
                else:  # Если не удалось отправить уведомление.
                    return redirect(
                        reverse('builds:order_confirmation') + '?success=False'
                    )  # Перенаправляем на страницу подтверждения с параметром success=False.

        except Exception as e:  # Если произошла ошибка при оформлении заказа.
            messages.error(request, f"Ошибка при оформлении заказа: {e}")  # Выводим сообщение об ошибке.
            print(
                f"Ошибка оформления заказа: {e}"
            )  # Выводим сообщение об ошибке в консоль.

    return render(
        request,
        'builds/checkout.html',
        {'cart_items': cart_items, 'total_price': total_price},
    )  # Отображаем страницу оформления заказа.


@login_required  # Требуется авторизация пользователя.
def order_confirmation(request):
    """Отображает страницу подтверждения заказа."""
    success = request.GET.get('success')  # Получаем параметр success из GET запроса.
    track_number = request.GET.get(
        'track_number'
    )  # Получаем трек-номер из GET запроса.
    if success == 'True':  # Если заказ успешно оформлен.
        messages.success(
            request,
            f"Заказ успешно оформлен! Проверьте вашу электронную почту. "
            f"Ваш трек-номер: {track_number}",
        )  # Выводим сообщение об успехе.
    elif success == 'False':  # Если не удалось отправить уведомление.
        messages.error(
            request, "Заказ оформлен, но не удалось отправить уведомление."
        )  # Выводим сообщение об ошибке.

    return render(
        request,
        'builds/order_confirmation.html',
        {'track_number': track_number},
    )  # Отображаем страницу подтверждения заказа.


@login_required  # Требуется авторизация пользователя.
def my_orders(request):
    """Отображает список заказов текущего пользователя."""
    orders = Order.objects.filter(
        user=request.user, is_completed=False
    ).order_by(
        '-order_date'
    )  # Получаем все незавершенные заказы текущего пользователя и сортируем по дате (от новых к старым).
    return render(
        request, 'builds/my_orders.html', {'orders': orders}
    )  # Отображаем страницу со списком заказов.


@cache_page(
    60 * 15
)  # Cache for 15 minutes # Кэшируем страницу на 15 минут (60 секунд * 15).
def index(request):
    """Отображает главную страницу."""
    cpu_list = CPU.objects.all().select_related()  # Получаем все процессоры.
    paginator = Paginator(
        cpu_list, 6
    )  # Создаем объект Paginator, разбивающий процессоры на страницы по 6 штук.

    page = request.GET.get('page')  # Получаем номер текущей страницы.
    try:
        cpus = paginator.page(
            page
        )  # Получаем объект Page для текущей страницы.
    except PageNotAnInteger:
        cpus = paginator.page(
            1
        )  # Если номер страницы не является целым числом, получаем первую страницу.
    except EmptyPage:
        cpus = paginator.page(
            paginator.num_pages
        )  # Если номер страницы больше, чем общее количество страниц, получаем последнюю страницу.

    context = {'cpus': cpus}  # Создаем контекст для шаблона.

    if request.user.is_authenticated:  # Если пользователь авторизован.
        if is_employee(
            request.user
        ):  # Если пользователь является сотрудником.
            return render(
                request, 'pc_builder/employee_index.html', context
            )  # Отображаем страницу для сотрудников.
        else:  # Если пользователь не является сотрудником.
            return render(
                request, 'pc_builder/index.html', context
            )  # Отображаем обычную главную страницу.
    else:  # Если пользователь не авторизован.
        return render(
            request, 'pc_builder/index.html', context
        )  # Отображаем обычную главную страницу.


def get_compatible_motherboards(request):
    """
    Возвращает JSON с материнскими платами, совместимыми с выбранным CPU.
    """
    cpu_id = request.GET.get('cpu_id')  # Получаем ID процессора из GET запроса.
    if cpu_id:  # Если ID процессора указан.
        try:
            cpu = CPU.objects.get(
                pk=cpu_id
            )  # Получаем процессор по ID. Если не найден, вызывается исключение.
            # Получаем материнские платы с тем же сокетом, что и у CPU
            compatible_motherboards = (
                Motherboard.objects.filter(socket=cpu.socket)
                .values('id', 'name')  # .values() для оптимизации
                        )  # Получаем материнские платы с тем же сокетом, что и у CPU. .values('id', 'name') используется для оптимизации запроса и получения только необходимых полей.
            return JsonResponse(
                list(compatible_motherboards), safe=False
            )  # Преобразуем QuerySet в список и возвращаем JSON ответ. safe=False позволяет сериализовать не-словарь.
        except CPU.DoesNotExist:  # Если процессор не найден.
            return JsonResponse(
                {'error': 'CPU не найден'}, status=404
            )  # Возвращаем JSON ответ с ошибкой.
    else:  # Если ID процессора не указан.
        return JsonResponse(
            {'error': 'Не указан CPU ID'}, status=400
        )  # Возвращаем JSON ответ с ошибкой.


def get_compatible_rams(request):
    """
    Возвращает JSON с RAM, совместимой с выбранной материнской платой.
    """
    motherboard_id = request.GET.get(
        'motherboard_id'
    )  # Получаем ID материнской платы из GET запроса.
    if motherboard_id:  # Если ID материнской платы указан.
        try:
            motherboard = Motherboard.objects.get(
                pk=motherboard_id
            )  # Получаем материнскую плату по ID. Если не найдена, вызывается исключение.
            # Получаем RAM с тем же типом и поддерживаемой частотой, что и у материнской платы
            compatible_rams = (
                RAM.objects.filter(
                    ram_type=motherboard.ram_type,
                    memory_clock__lte=motherboard.max_ram_speed,
                )
                .values('id', 'name')
            )  # Получаем оперативную память с тем же типом и поддерживаемой частотой, что и у материнской платы. .values('id', 'name') используется для оптимизации запроса и получения только необходимых полей.
            return JsonResponse(
                list(compatible_rams), safe=False
            )  # Преобразуем QuerySet в список и возвращаем JSON ответ. safe=False позволяет сериализовать не-словарь.
        except Motherboard.DoesNotExist:  # Если материнская плата не найдена.
            return JsonResponse(
                {'error': 'Motherboard не найдена'}, status=404
            )  # Возвращаем JSON ответ с ошибкой.
    else:  # Если ID материнской платы не указан.
        return JsonResponse(
            {'error': 'Не указан Motherboard ID'}, status=400
        )  # Возвращаем JSON ответ с ошибкой.


def get_compatible_cpu(request):
    """
    Возвращает JSON с CPU, совместимыми с выбранной материнской платой.
    """
    motherboard_id = request.GET.get(
        'motherboard_id'
    )  # Получаем ID материнской платы из GET запроса.
    if motherboard_id:  # Если ID материнской платы указан.
        try:
            motherboard = Motherboard.objects.get(
                pk=motherboard_id
            )  # Получаем материнскую плату по ID. Если не найдена, вызывается исключение.
            # Получаем CPU с тем же сокетом, что и у материнской платы
            compatible_cpus = (
                CPU.objects.filter(socket=motherboard.socket)
                .values('id', 'name')
            )  # Получаем процессоры с тем же сокетом, что и у материнской платы. .values('id', 'name') используется для оптимизации запроса и получения только необходимых полей.
            return JsonResponse(
                list(compatible_cpus), safe=False
            )  # Преобразуем QuerySet в список и возвращаем JSON ответ. safe=False позволяет сериализовать не-словарь.
        except Motherboard.DoesNotExist:  # Если материнская плата не найдена.
            return JsonResponse(
                {'error': 'Motherboard не найдена'}, status=404
            )  # Возвращаем JSON ответ с ошибкой.
    else:  # Если ID материнской платы не указан.
        return JsonResponse(
            {'error': 'Не указан Motherboard ID'}, status=400
        )  # Возвращаем JSON ответ с ошибкой.


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee).
def employee_out_of_stock_list(request):
    """Представление для отображения списка товаров, которых нет в наличии."""
    out_of_stock_items = Stock.objects.filter(
        quantity=0
    )  # Получаем все товары, которых нет в наличии (quantity = 0).

    return render(
        request,
        'builds/employee_out_of_stock_list.html',
        {'out_of_stock_items': out_of_stock_items},
    )  # Отображаем страницу со списком товаров, которых нет в наличии.
 