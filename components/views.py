# components/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)  # Импортируем классы для пагинации
from django.db.models import Q  # Импортируем Q для сложных запросов
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)  # Импортируем декораторы для проверки авторизации и прав пользователя
from django.http import (
    HttpResponseRedirect,
)  # Импортируем класс для перенаправления
from django.urls import reverse  # Импортируем reverse для получения URL по имени
from .models import (
    CPU,
    GPU,
    Motherboard,
    RAM,
    Storage,
    PSU,
    Case,
    Cooler,
    Stock,
    Manufacturer,
)  # Импортируем модели компонентов и производителя
from .forms import (
    CPUSearchForm,
    GPUSearchForm,
    MotherboardSearchForm,
    RAMSearchForm,
    StorageSearchForm,
    PSUSearchForm,
    CaseSearchForm,
    CoolerSearchForm,
    ReviewForm,
)  # Импортируем формы поиска компонентов и форму отзыва
from django.shortcuts import render, get_object_or_404
from django.shortcuts import (
    redirect,
)  # Import all search forms # Импортируем функцию redirect

def cpu_list(request):
    """Отображает список процессоров с возможностью фильтрации и поиска."""
    form = CPUSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска CPU, передавая параметры из GET запроса
    cpus_list = CPU.objects.all()  # Получаем все процессоры из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        socket = form.cleaned_data.get(
            'socket'
        )  # Получаем выбранный сокет из очищенных данных формы
        integrated_graphics = form.cleaned_data.get(
            'integrated_graphics'
        )  # Получаем значение флага "интегрированная графика" из очищенных данных формы
        sort = form.cleaned_data.get(
            'sort'
        )  # Получаем значение сортировки

        if q:  # Если есть поисковой запрос
            cpus_list = cpus_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем процессоры по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты

        if manufacturers:  # Если выбраны производители
            cpus_list = cpus_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем процессоры по выбранным производителям

        if socket:  # Если выбран сокет
            cpus_list = cpus_list.filter(
                socket__icontains=socket
            )  # Фильтруем процессоры по выбранному сокету

        if integrated_graphics:  # Если установлен флаг "интегрированная графика"
            cpus_list = cpus_list.filter(
                integrated_graphics=True
            )  # Фильтруем процессоры, у которых есть интегрированная графика

        # Сортировка по параметру sort
        if sort == 'price_asc':
            cpus_list = cpus_list.order_by(
                'price'
            )  # Сортируем процессоры по возрастанию цены
        elif sort == 'price_desc':
            cpus_list = cpus_list.order_by(
                '-price'
            )  # Сортируем процессоры по убыванию цены
        elif sort == 'frequency_desc':
            cpus_list = cpus_list.order_by(
                '-frequency'
            )  # Сортируем процессоры по убыванию частоты
        else:
            # По умолчанию — популярность (например, по количеству заказов или рейтингу)
            # Если у вас нет поля популярности, можно убрать или заменить на id
            cpus_list = cpus_list.order_by(
                '-id'
            )  # Сортируем процессоры по id в обратном порядке (новые в начале)

    # Получаем наличие из Stock
    stock_items = Stock.objects.filter(
        component_type='cpu'
    )  # Получаем все записи о наличии для процессоров
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        cpus_list, 6
    )  # Создаем объект Paginator, разбивающий список процессоров на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        cpus = paginator.page(page)  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        cpus = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        cpus = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    context = {
        'cpus': cpus,
        'form': form,
        'stock_dict': stock_dict,
    }  # Создаем контекст для шаблона, передавая список процессоров, форму поиска и словарь наличия
    return render(
        request, 'components/cpu_list.html', context
    )  # Отображаем шаблон списка процессоров, передавая контекст

def gpu_list(request):
    """Отображает список видеокарт с возможностью фильтрации и поиска."""
    form = GPUSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска GPU, передавая параметры из GET запроса
    gpus_list = GPU.objects.all()  # Получаем все видеокарты из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        memory = form.cleaned_data.get(
            'memory'
        )  # Получаем выбранный объем памяти из очищенных данных формы
        interface = form.cleaned_data.get(
            'interface'
        )  # Получаем выбранный интерфейс из очищенных данных формы

        if q:  # Если есть поисковой запрос
            gpus_list = gpus_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем видеокарты по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Если выбраны производители
            gpus_list = gpus_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем видеокарты по выбранным производителям
        if memory:  # Если выбран объем памяти
            gpus_list = gpus_list.filter(
                memory=memory
            )  # Фильтруем видеокарты по выбранному объему памяти
        if interface:  # Если выбран интерфейс
            gpus_list = gpus_list.filter(
                interface__icontains=interface
            )  # Фильтруем видеокарты по выбранному интерфейсу

    # Get all Stock objects for GPUs
    stock_items = Stock.objects.filter(
        component_type='gpu'
    )  # Получаем все записи о наличии для видеокарт
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        gpus_list, 6
    )  # Создаем объект Paginator, разбивающий список видеокарт на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        gpus = paginator.page(page)  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        gpus = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        gpus = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/gpu_list.html',
        {'gpus': gpus, 'form': form, 'stock_dict': stock_dict},
    )  # Отображаем шаблон списка видеокарт, передавая контекст


def motherboard_list(request):
    """Отображает список материнских плат с возможностью фильтрации и поиска."""
    form = MotherboardSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска материнских плат, передавая параметры из GET запроса
    motherboards_list = Motherboard.objects.all()  # Получаем все материнские платы из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        socket = form.cleaned_data.get(
            'socket'
        )  # Получаем выбранный сокет из очищенных данных формы
        form_factor = form.cleaned_data.get(
            'form_factor'
        )  # Получаем выбранный форм-фактор из очищенных данных формы

        if q:  # Если есть поисковой запрос
            motherboards_list = motherboards_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем материнские платы по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Если выбраны производители
            motherboards_list = motherboards_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем материнские платы по выбранным производителям
        if socket:  # Если выбран сокет
            motherboards_list = motherboards_list.filter(
                socket__icontains=socket
            )  # Фильтруем материнские платы по выбранному сокету
        if form_factor:  # Если выбран форм-фактор
            motherboards_list = motherboards_list.filter(
                form_factor__icontains=form_factor
            )  # Фильтруем материнские платы по выбранному форм-фактору

    # Get all Stock objects for Motherboards
    stock_items = Stock.objects.filter(
        component_type='motherboard'
    )  # Получаем все записи о наличии для материнских плат
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        motherboards_list, 6
    )  # Создаем объект Paginator, разбивающий список материнских плат на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        motherboards = paginator.page(
            page
        )  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        motherboards = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        motherboards = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/motherboard_list.html',
        {
            'motherboards': motherboards,
            'form': form,
            'stock_dict': stock_dict,
        },
    )  # Отображаем шаблон списка материнских плат, передавая контекст


def ram_list(request):
    """Отображает список оперативной памяти с возможностью фильтрации и поиска."""
    form = RAMSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска RAM, передавая параметры из GET запроса
    rams_list = RAM.objects.all()  # Получаем все модули оперативной памяти из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        type = form.cleaned_data.get(
            'type'
        )  # Получаем выбранный тип памяти из очищенных данных формы
        capacity = form.cleaned_data.get(
            'capacity'
        )  # Получаем выбранную емкость памяти из очищенных данных формы

        if q:  # Если есть поисковой запрос
            rams_list = rams_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем модули памяти по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Если выбраны производители
            rams_list = rams_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем модули памяти по выбранным производителям
        if type:  # Если выбран тип памяти
            rams_list = rams_list.filter(
                type__icontains=type
            )  # Фильтруем модули памяти по выбранному типу
        if capacity:  # Если выбрана емкость
            rams_list = rams_list.filter(
                capacity=capacity
            )  # Фильтруем модули памяти по выбранной емкости

    # Get all Stock objects for RAM
    stock_items = Stock.objects.filter(
        component_type='ram'
    )  # Получаем все записи о наличии для модулей памяти
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        rams_list, 6
    )  # Создаем объект Paginator, разбивающий список модулей памяти на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        rams = paginator.page(page)  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        rams = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        rams = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/ram_list.html',
        {'rams': rams, 'form': form, 'stock_dict': stock_dict},
    )  # Отображаем шаблон списка модулей памяти, передавая контекст


def storage_list(request):
    """Отображает список накопителей с возможностью фильтрации и поиска."""
    form = StorageSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска накопителей, передавая параметры из GET запроса
    storages_list = Storage.objects.all()  # Получаем все накопители из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        type = form.cleaned_data.get(
            'type'
        )  # Получаем выбранный тип накопителя из очищенных данных формы
        capacity = form.cleaned_data.get(
            'capacity'
        )  # Получаем выбранную емкость накопителя из очищенных данных формы

        if q:  # Если есть поисковой запрос
            storages_list = storages_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем накопители по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Если выбраны производители
            storages_list = storages_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем накопители по выбранным производителям
        if type:  # Если выбран тип накопителя
            storages_list = storages_list.filter(
                type__icontains=type
            )  # Фильтруем накопители по выбранному типу
        if capacity:  # Если выбрана емкость
            storages_list = storages_list.filter(
                capacity=capacity
            )  # Фильтруем накопители по выбранной емкости

    # Get all Stock objects for Storages
    stock_items = Stock.objects.filter(
        component_type='storage'
    )  # Получаем все записи о наличии для накопителей
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        storages_list, 6
    )  # Создаем объект Paginator, разбивающий список накопителей на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        storages = paginator.page(
            page
        )  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        storages = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        storages = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/storage_list.html',
        {
            'storages': storages,
            'form': form,
            'stock_dict': stock_dict,
        },
    )  # Отображаем шаблон списка накопителей, передавая контекст


def psu_list(request):
    """Отображает список блоков питания с возможностью фильтрации и поиска."""
    form = PSUSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска блоков питания, передавая параметры из GET запроса
    psus_list = PSU.objects.all()  # Получаем все блоки питания из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        power = form.cleaned_data.get(
            'power'
        )  # Получаем выбранную мощность из очищенных данных формы
        certification = form.cleaned_data.get(
            'certification'
        )  # Получаем выбранный сертификат из очищенных данных формы

        if q:  # Если есть поисковой запрос
            psus_list = psus_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем блоки питания по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Если выбраны производители
            psus_list = psus_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем блоки питания по выбранным производителям
        if power:  # Если выбрана мощность
            psus_list = psus_list.filter(
                power=power
            )  # Фильтруем блоки питания по выбранной мощности
        if certification:  # Если выбран сертификат
            psus_list = psus_list.filter(
                certification__icontains=certification
            )  # Фильтруем блоки питания по выбранному сертификату

    # Get all Stock objects for PSUs
    stock_items = Stock.objects.filter(
        component_type='psu'
    )  # Получаем все записи о наличии для блоков питания
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        psus_list, 6
    )  # Создаем объект Paginator, разбивающий список блоков питания на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        psus = paginator.page(page)  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        psus = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        psus = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/psu_list.html',
        {'psus': psus, 'form': form, 'stock_dict': stock_dict},
    )  # Отображаем шаблон списка блоков питания, передавая контекст


def case_list(request):
    """Отображает список корпусов с возможностью фильтрации и поиска."""
    form = CaseSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска корпусов, передавая параметры из GET запроса
    cases_list = Case.objects.all()  # Получаем все корпуса из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        form_factor = form.cleaned_data.get(
            'form_factor'
        )  # Получаем выбранный форм-фактор из очищенных данных формы
        dimensions = form.cleaned_data.get(
            'dimensions'
        )  # Получаем выбранные размеры из очищенных данных формы
        side_panel_window = form.cleaned_data.get(
            'side_panel_window'
        )  # Получаем значение флага "боковое окно" из очищенных данных формы

        if q:  # Если есть поисковой запрос
            cases_list = cases_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем корпуса по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Если выбраны производители
            cases_list = cases_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем корпуса по выбранным производителям
        if form_factor:  # Если выбран форм-фактор
            cases_list = cases_list.filter(
                form_factor__icontains=form_factor
            )  # Фильтруем корпуса по выбранному форм-фактору
        if dimensions:  # Если выбраны размеры
            cases_list = cases_list.filter(
                dimensions__icontains=dimensions
            )  # Фильтруем корпуса по выбранным размерам
        if side_panel_window:  # Если установлен флаг "боковое окно"
            cases_list = cases_list.filter(
                side_panel_window=True
            )  # Фильтруем корпуса, у которых есть боковое окно

    # Get all Stock objects for Cases
    stock_items = Stock.objects.filter(
        component_type='case'
    )  # Получаем все записи о наличии для корпусов
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        cases_list, 6
    )  # Создаем объект Paginator, разбивающий список корпусов на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        cases = paginator.page(page)  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        cases = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        cases = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/case_list.html',
        {'cases': cases, 'form': form, 'stock_dict': stock_dict},
    )  # Отображаем шаблон списка корпусов, передавая контекст


def cooler_list(request):
    """Отображает список систем охлаждения с возможностью фильтрации и поиска."""
    form = CoolerSearchForm(
        request.GET
    )  # Создаем экземпляр формы поиска систем охлаждения, передавая параметры из GET запроса
    coolers_list = Cooler.objects.all()  # Получаем все системы охлаждения из базы данных

    if form.is_valid():  # Проверяем, прошла ли форма валидацию
        q = form.cleaned_data.get(
            'q'
        )  # Получаем поисковой запрос из очищенных данных формы
        manufacturers = form.cleaned_data.get(
            'manufacturer'
        )  # Получаем выбранных производителей из очищенных данных формы
        cooler_type = form.cleaned_data.get(
            'cooler_type'
        )  # Получаем выбранный тип системы охлаждения из очищенных данных формы
        fan_size = form.cleaned_data.get(
            'fan_size'
        )  # Получаем выбранный размер вентилятора из очищенных данных формы
        rgb = form.cleaned_data.get(
            'rgb'
        )  # Получаем значение флага "RGB подсветка" из очищенных данных формы

        if q:  # Если есть поисковой запрос
            coolers_list = coolers_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()  # Фильтруем системы охлаждения по производителю или модели, используя поисковой запрос
                                # Q позволяет делать сложные запросы с использованием "или" ( | )
                                # distinct() убирает дубликаты
        if manufacturers:  # Check if manufacturer is selected
            coolers_list = coolers_list.filter(
                manufacturer__id__in=manufacturers
            )  # Фильтруем системы охлаждения по выбранным производителям
        if cooler_type:  # Если выбран тип системы охлаждения
            coolers_list = coolers_list.filter(
                cooler_type=cooler_type
            )  # Фильтруем системы охлаждения по выбранному типу
        if fan_size:  # Если выбран размер вентилятора
            coolers_list = coolers_list.filter(
                fan_size=fan_size
            )  # Фильтруем системы охлаждения по выбранному размеру вентилятора
        if rgb:  # Если установлен флаг "RGB подсветка"
            coolers_list = coolers_list.filter(
                rgb=rgb
            )  # Фильтруем системы охлаждения, у которых есть RGB подсветка

    # Get all Stock objects for Coolers
    stock_items = Stock.objects.filter(
        component_type='cooler'
    )  # Получаем все записи о наличии для систем охлаждения
    stock_dict = {
        item.component_id: item for item in stock_items
    }  # Создаем словарь, где ключ - ID компонента, значение - объект Stock

    paginator = Paginator(
        coolers_list, 6
    )  # Создаем объект Paginator, разбивающий список систем охлаждения на страницы по 6 штук
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET запроса
    try:
        coolers = paginator.page(
            page
        )  # Получаем объект Page для текущей страницы
    except PageNotAnInteger:  # Если номер страницы не является целым числом
        coolers = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом)
    except EmptyPage:  # Если запрошенная страница не существует
        coolers = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц)

    return render(
        request,
        'components/cooler_list.html',
        {
            'coolers': coolers,
            'form': form,
            'stock_dict': stock_dict,
        },
    )  # Отображаем шаблон списка систем охлаждения, передавая контекст


def get_stock_status(component_type, component_id):
    """
    Получает статус наличия товара на складе.
    Возвращает True, если товар есть в наличии, False - если нет.
    """
    try:
        stock = Stock.objects.get(
            component_type=component_type, component_id=component_id
        )  # Получаем информацию о наличии товара на складе по типу и ID компонента.
        return (
            stock.quantity > 0
        )  # Возвращаем True, если количество товара на складе больше нуля, и False в противном случае.
    except Stock.DoesNotExist:
        return (
            False
        )  # Или True, если отсутствие записи означает наличие на складе. Возвращаем False, если информация о наличии товара не найдена.


def cpu_detail(request, pk):
    """Отображает детальную информацию о процессоре."""
    cpu = get_object_or_404(
        CPU, pk=pk
    )  # Получаем процессор по ID или возвращаем 404, если не найден.
    try:
        stock = Stock.objects.get(
            component_type='cpu', component_id=cpu.id
        )  # Пытаемся получить информацию о наличии процессора на складе.
        stock_quantity = stock.quantity  # Получаем количество процессоров на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли процессор в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/cpu_detail.html',
        {
            'cpu': cpu,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о процессоре.


def gpu_detail(request, pk):
    """Отображает детальную информацию о видеокарте."""
    gpu = get_object_or_404(
        GPU, pk=pk
    )  # Получаем видеокарту по ID или возвращаем 404, если не найдена.
    try:
        stock = Stock.objects.get(
            component_type='gpu', component_id=gpu.id
        )  # Пытаемся получить информацию о наличии видеокарты на складе.
        stock_quantity = stock.quantity  # Получаем количество видеокарт на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли видеокарта в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/gpu_detail.html',
        {
            'gpu': gpu,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о видеокарте.


def motherboard_detail(request, pk):
    """Отображает детальную информацию о материнской плате."""
    motherboard = get_object_or_404(
        Motherboard, pk=pk
    )  # Получаем материнскую плату по ID или возвращаем 404, если не найдена.
    try:
        stock = Stock.objects.get(
            component_type='motherboard', component_id=motherboard.id
        )  # Пытаемся получить информацию о наличии материнской платы на складе.
        stock_quantity = (
            stock.quantity
        )  # Получаем количество материнских плат на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли материнская плата в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/motherboard_detail.html',
        {
            'motherboard': motherboard,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о материнской плате.


def ram_detail(request, pk):
    """Отображает детальную информацию об оперативной памяти."""
    ram = get_object_or_404(
        RAM, pk=pk
    )  # Получаем модуль оперативной памяти по ID или возвращаем 404, если не найден.
    try:
        stock = Stock.objects.get(
            component_type='ram', component_id=ram.id
        )  # Пытаемся получить информацию о наличии модуля памяти на складе.
        stock_quantity = stock.quantity  # Получаем количество модулей памяти на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли модуль памяти в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/ram_detail.html',
        {
            'ram': ram,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о модуле памяти.


def storage_detail(request, pk):
    """Отображает детальную информацию о накопителе."""
    storage = get_object_or_404(
        Storage, pk=pk
    )  # Получаем накопитель по ID или возвращаем 404, если не найден.
    try:
        stock = Stock.objects.get(
            component_type='storage', component_id=storage.id
        )  # Пытаемся получить информацию о наличии накопителя на складе.
        stock_quantity = stock.quantity  # Получаем количество накопителей на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли накопитель в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/storage_detail.html',
        {
            'storage': storage,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о накопителе.


def psu_detail(request, pk):
    """Отображает детальную информацию о блоке питания."""
    psu = get_object_or_404(
        PSU, pk=pk
    )  # Получаем блок питания по ID или возвращаем 404, если не найден.
    try:
        stock = Stock.objects.get(
            component_type='psu', component_id=psu.id
        )  # Пытаемся получить информацию о наличии блока питания на складе.
        stock_quantity = stock.quantity  # Получаем количество блоков питания на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли блок питания в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/psu_detail.html',
        {
            'psu': psu,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о блоке питания.


def case_detail(request, pk):
    """Отображает детальную информацию о корпусе."""
    case = get_object_or_404(
        Case, pk=pk
    )  # Получаем корпус по ID или возвращаем 404, если не найден.
    try:
        stock = Stock.objects.get(
            component_type='case', component_id=case.id
        )  # Пытаемся получить информацию о наличии корпуса на складе.
        stock_quantity = stock.quantity  # Получаем количество корпусов на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли корпус в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/case_detail.html',
        {
            'case': case,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о корпусе.


def cooler_detail(request, pk):
    """Отображает детальную информацию о системе охлаждения."""
    cooler = get_object_or_404(
        Cooler, pk=pk
    )  # Получаем систему охлаждения по ID или возвращаем 404, если не найдена.
    try:
        stock = Stock.objects.get(
            component_type='cooler', component_id=cooler.id
        )  # Пытаемся получить информацию о наличии системы охлаждения на складе.
        stock_quantity = stock.quantity  # Получаем количество систем охлаждения на складе.
        in_stock = (
            stock_quantity > 0
        )  # Определяем, есть ли система охлаждения в наличии (количество > 0).
    except Stock.DoesNotExist:  # Если информация о наличии не найдена.
        in_stock = False  # Устанавливаем флаг "в наличии" в False.
        stock_quantity = 0  # Устанавливаем количество на складе в 0.
    review_form = (
        ReviewForm()
    )  # Создаем экземпляр формы для добавления отзыва.
    return render(
        request,
        'components/cooler_detail.html',
        {
            'cooler': cooler,
            'review_form': review_form,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        },
    )  # Отображаем страницу с детальной информацией о системе охлаждения.


@login_required  # Требуется авторизация пользователя.
def add_review(request, pk, component_type):
    """Добавляет отзыв к компоненту."""
    if request.method == 'POST':  # Если это POST запрос.
        form = ReviewForm(
            request.POST
        )  # Создаем экземпляр формы для добавления отзыва, передавая данные из POST запроса.
        if form.is_valid():  # Если форма валидна.
            review = form.save(
                commit=False
            )  # Создаем объект отзыва, но не сохраняем его в базу данных.
            review.user = request.user  # Устанавливаем пользователя, оставившего отзыв.

            if component_type == 'cpu':  # Если тип компонента - процессор.
                component = get_object_or_404(
                    CPU, pk=pk
                )  # Получаем процессор по ID или возвращаем 404, если не найден.
            elif component_type == 'gpu':  # Если тип компонента - видеокарта.
                component = get_object_or_404(
                    GPU, pk=pk
                )  # Получаем видеокарту по ID или возвращаем 404, если не найдена.
            elif component_type == 'motherboard':  # Если тип компонента - материнская плата.
                component = get_object_or_404(
                    Motherboard, pk=pk
                )  # Получаем материнскую плату по ID или возвращаем 404, если не найдена.
            elif component_type == 'ram':  # Если тип компонента - оперативная память.
                component = get_object_or_404(
                    RAM, pk=pk
                )  # Получаем модуль памяти по ID или возвращаем 404, если не найден.
            elif component_type == 'storage':  # Если тип компонента - накопитель.
                component = get_object_or_404(
                    Storage, pk=pk
                )  # Получаем накопитель по ID или возвращаем 404, если не найден.
            elif component_type == 'psu':  # Если тип компонента - блок питания.
                component = get_object_or_404(
                    PSU, pk=pk
                )  # Получаем блок питания по ID или возвращаем 404, если не найден.
            elif component_type == 'case':  # Если тип компонента - корпус.
                component = get_object_or_404(
                    Case, pk=pk
                )  # Получаем корпус по ID или возвращаем 404, если не найден.
            elif component_type == 'cooler':  # Если тип компонента - система охлаждения.
                component = get_object_or_404(
                    Cooler, pk=pk
                )  # Получаем систему охлаждения по ID или возвращаем 404, если не найдена.
            else:  # Если тип компонента неверный.
                raise ValueError("Неверный тип компонента")  # Вызываем исключение.

            if component:  # Если компонент найден.
                review.content_object = (
                    component  # Устанавливаем компонент, к которому относится отзыв.
                )
                review.save()  # Сохраняем отзыв в базу данных.
                # Construct the URL based on the component type and ID.
                return redirect(
                    reverse(
                        f'components:{component_type}_detail', kwargs={'pk': pk}
                    )
                )  # Перенаправляем на страницу с детальной информацией о компоненте.
            else:
                # Handle the case where no component was found.  This should ideally never happen
                # given the get_object_or_404 calls, but it's good to be defensive.
                return redirect(
                    'home'
                )  # Or some other safe default. # Обрабатываем случай, когда компонент не найден.
        else:
            # Если форма не валидна, нужно передать ее обратно в шаблон, чтобы показать ошибки.
            # Determine the component type and ID to render the detail template correctly
            if component_type == 'cpu':
                component = get_object_or_404(CPU, pk=pk)
                template = 'components/cpu_detail.html'
            # (Add similar blocks for other component types)
            else:
                # Fallback if no component found or if there's an error in the component_type
                return redirect('home')

            return render(request, template, {'component': component, 'review_form': form})

    else:
        # Если метод не POST, это ошибка.  Нужно перенаправить пользователя или показать страницу с ошибкой.
        return (
            redirect('home')
        )  # Или другая подходящая страница. # Если метод не POST, перенаправляем пользователя на главную страницу.


def is_employee(user):  # Assuming you have this function
    """Проверяет, является ли пользователь сотрудником."""
    return user.is_staff  # Возвращает True, если пользователь является сотрудником (is_staff=True).


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    lambda u: u.is_staff
)  # Требуется, чтобы пользователь был сотрудником (проверка через анонимную функцию).
def replenish_stock_item(request, pk):
    """Пополняет запас выбранного элемента на 10."""
    stock_item = get_object_or_404(
        Stock, pk=pk
    )  # Получаем информацию о наличии товара на складе по ID или возвращаем 404, если не найдена.
    stock_item.quantity += (
        10  # Увеличиваем количество товара на складе на 10.
    )
    stock_item.save()  # Сохраняем изменения в базе данных.

    # Get the out of stock count after replenishing
    out_of_stock_count = Stock.objects.filter(quantity=0).count()

    # Redirect with the out_of_stock_count as a query parameter
    url = reverse('components:stock_list') + f'?out_of_stock_count={out_of_stock_count}'
    return HttpResponseRedirect(url)  # Перенаправляем на страницу со списком товаров с информацией об измененном количестве отсутствующих товаров.


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    is_employee
)  # Требуется, чтобы пользователь был сотрудником (проверка через функцию is_employee).
def reduce_stock_item(request, pk):
    """Уменьшает запас выбранного элемента на 10."""
    stock_item = get_object_or_404(
        Stock, pk=pk
    )  # Получаем информацию о наличии товара на складе по ID или возвращаем 404, если не найдена.
    stock_item.quantity -= (
        10  # Уменьшаем количество товара на складе на 10.
    )
    if stock_item.quantity < 0:  # Если количество товара стало отрицательным.
        stock_item.quantity = (
            0  # Предотвращаем отрицательное количество. Устанавливаем количество товара в 0.
        )
    stock_item.save()  # Сохраняем изменения в базе данных.
    return HttpResponseRedirect(
        reverse('components:stock_list')
    )  # Перенаправляем на страницу со списком товаров.


@login_required  # Требуется авторизация пользователя.
@user_passes_test(
    lambda u: u.is_staff
)  # Требуется, чтобы пользователь был сотрудником (проверка через анонимную функцию).
def stock_list_view(request):
    """Отображает список товаров на складе с возможностью поиска."""
    query = request.GET.get(
        'q'
    )  # Получаем поисковой запрос из GET параметров.
    stock_items = Stock.objects.all()  # Получаем все записи о наличии товаров на складе.

    if query:  # Если есть поисковой запрос.
        filtered_stock_items = []  # Создаем пустой список для отфильтрованных записей.
        for stock_item in stock_items:  # Для каждой записи о наличии товара на складе.
            component = None  # Инициализируем переменную для компонента.
            try:
                if (
                    stock_item.component_type == 'cpu'
                ):  # Если тип компонента - процессор.
                    component = CPU.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем процессор по ID.
                elif (
                    stock_item.component_type == 'gpu'
                ):  # Если тип компонента - видеокарта.
                    component = GPU.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем видеокарту по ID.
                elif (
                    stock_item.component_type == 'motherboard'
                ):  # Если тип компонента - материнская плата.
                    component = Motherboard.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем материнскую плату по ID.
                elif (
                    stock_item.component_type == 'ram'
                ):  # Если тип компонента - оперативная память.
                    component = RAM.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем модуль памяти по ID.
                elif (
                    stock_item.component_type == 'storage'
                ):  # Если тип компонента - накопитель.
                    component = Storage.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем накопитель по ID.
                elif (
                    stock_item.component_type == 'psu'
                ):  # Если тип компонента - блок питания.
                    component = PSU.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем блок питания по ID.
                elif (
                    stock_item.component_type == 'case'
                ):  # Если тип компонента - корпус.
                    component = Case.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем корпус по ID.
                elif (
                    stock_item.component_type == 'cooler'
                ):  # Если тип компонента - система охлаждения.
                    component = Cooler.objects.get(
                        pk=stock_item.component_id
                    )  # Получаем систему охлаждения по ID.

                if component:  # Если компонент найден.
                    component_name = (
                        f"{component.manufacturer} {component.model}"  # Получаем имя компонента
                    )
                    if (
                        query.lower() in component_name.lower()
                    ) or (
                        query.lower() in str(stock_item.quantity).lower()
                    ):  # добавил поиск по quantity
                        filtered_stock_items.append(
                            stock_item
                        )  # Если поисковой запрос содержится в имени компонента или количестве, добавляем запись в отфильтрованный список.

            except (
                CPU.DoesNotExist,
                GPU.DoesNotExist,
                Motherboard.DoesNotExist,
                RAM.DoesNotExist,
                Storage.DoesNotExist,
                PSU.DoesNotExist,
                Case.DoesNotExist,
                Cooler.DoesNotExist,
            ):  # Если компонент не найден.
                pass  # Просто игнорируем, если компонент не найден

        stock_items = (
            filtered_stock_items  # Заменяем stock_items отфильтрованным списком
        )

    paginator = Paginator(
        stock_items, 10
    )  # Создаем объект Paginator, разбивающий список товаров на складе на страницы по 10 штук.
    page = request.GET.get('page')  # Получаем номер текущей страницы из GET параметров.
    try:
        stock_items = paginator.get_page(
            page
        )  # Получаем объект Page для текущей страницы.
    except PageNotAnInteger:  # Если номер страницы не является целым числом.
        stock_items = paginator.page(
            1
        )  # Получаем первую страницу (если номер страницы не указан или не является числом).
    except EmptyPage:  # Если запрошенная страница не существует.
        stock_items = paginator.page(
            paginator.num_pages
        )  # Получаем последнюю страницу (если номер страницы больше, чем общее количество страниц).

    # Get out of stock count
    out_of_stock_count = Stock.objects.filter(quantity=0).count()


    context = {
        'stock_items': stock_items,
        'query': query,
        'out_of_stock_count': out_of_stock_count,
    }  # Создаем контекст для шаблона.
    return render(
        request, 'builds/stock_list.html', context
    )  # Отображаем страницу со списком товаров на складе.
