# components/views.py
# components/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
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
)
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
)
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect  # Import all search forms


def cpu_list(request):
    form = CPUSearchForm(request.GET)
    cpus_list = CPU.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        socket = form.cleaned_data.get('socket')
        integrated_graphics = form.cleaned_data.get('integrated_graphics')
        sort = form.cleaned_data.get('sort')  # Получаем значение сортировки

        if q:
            cpus_list = cpus_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()

        if manufacturers:
            cpus_list = cpus_list.filter(manufacturer__id__in=manufacturers)

        if socket:
            cpus_list = cpus_list.filter(socket__icontains=socket)

        if integrated_graphics:
            cpus_list = cpus_list.filter(integrated_graphics=True)

    # Сортировка по параметру sort
    if sort == 'price_asc':
        cpus_list = cpus_list.order_by('price')
    elif sort == 'price_desc':
        cpus_list = cpus_list.order_by('-price')
    elif sort == 'frequency_desc':
        cpus_list = cpus_list.order_by('-frequency')
    else:
        # По умолчанию — популярность (например, по количеству заказов или рейтингу)
        # Если у вас нет поля популярности, можно убрать или заменить на id
        cpus_list = cpus_list.order_by('-id')

    # Получаем наличие из Stock
    stock_items = Stock.objects.filter(component_type='cpu')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(cpus_list, 6)
    page = request.GET.get('page')
    try:
        cpus = paginator.page(page)
    except PageNotAnInteger:
        cpus = paginator.page(1)
    except EmptyPage:
        cpus = paginator.page(paginator.num_pages)

    context = {
        'cpus': cpus,
        'form': form,
        'stock_dict': stock_dict,
    }
    return render(request, 'components/cpu_list.html', context)


def gpu_list(request):
    form = GPUSearchForm(request.GET)
    gpus_list = GPU.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        memory = form.cleaned_data.get('memory')
        interface = form.cleaned_data.get('interface')

        if q:
            gpus_list = gpus_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:
            gpus_list = gpus_list.filter(manufacturer__id__in=manufacturers)
        if memory:
            gpus_list = gpus_list.filter(memory=memory)
        if interface:
            gpus_list = gpus_list.filter(interface__icontains=interface)

    # Get all Stock objects for GPUs
    stock_items = Stock.objects.filter(component_type='gpu')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(gpus_list, 6)
    page = request.GET.get('page')
    try:
        gpus = paginator.page(page)
    except PageNotAnInteger:
        gpus = paginator.page(1)
    except EmptyPage:
        gpus = paginator.page(paginator.num_pages)

    return render(
        request, 'components/gpu_list.html', {'gpus': gpus, 'form': form, 'stock_dict': stock_dict}
    )


def motherboard_list(request):
    form = MotherboardSearchForm(request.GET)
    motherboards_list = Motherboard.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        socket = form.cleaned_data.get('socket')
        form_factor = form.cleaned_data.get('form_factor')

        if q:
            motherboards_list = motherboards_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:
            motherboards_list = motherboards_list.filter(manufacturer__id__in=manufacturers)
        if socket:
            motherboards_list = motherboards_list.filter(socket__icontains=socket)
        if form_factor:
            motherboards_list = motherboards_list.filter(
                form_factor__icontains=form_factor
            )

    # Get all Stock objects for Motherboards
    stock_items = Stock.objects.filter(component_type='motherboard')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(motherboards_list, 6)
    page = request.GET.get('page')
    try:
        motherboards = paginator.page(page)
    except PageNotAnInteger:
        motherboards = paginator.page(1)
    except EmptyPage:
        motherboards = paginator.page(paginator.num_pages)

    return render(
        request,
        'components/motherboard_list.html',
        {'motherboards': motherboards, 'form': form, 'stock_dict': stock_dict},
    )


def ram_list(request):
    form = RAMSearchForm(request.GET)
    rams_list = RAM.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        type = form.cleaned_data.get('type')
        capacity = form.cleaned_data.get('capacity')

        if q:
            rams_list = rams_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:
            rams_list = rams_list.filter(manufacturer__id__in=manufacturers)
        if type:
            rams_list = rams_list.filter(type__icontains=type)
        if capacity:
            rams_list = rams_list.filter(capacity=capacity)

    # Get all Stock objects for RAM
    stock_items = Stock.objects.filter(component_type='ram')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(rams_list, 6)
    page = request.GET.get('page')
    try:
        rams = paginator.page(page)
    except PageNotAnInteger:
        rams = paginator.page(1)
    except EmptyPage:
        rams = paginator.page(paginator.num_pages)

    return render(
        request, 'components/ram_list.html', {'rams': rams, 'form': form, 'stock_dict': stock_dict}
    )


def storage_list(request):
    form = StorageSearchForm(request.GET)
    storages_list = Storage.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        type = form.cleaned_data.get('type')
        capacity = form.cleaned_data.get('capacity')

        if q:
            storages_list = storages_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:
            storages_list = storages_list.filter(manufacturer__id__in=manufacturers)
        if type:
            storages_list = storages_list.filter(type__icontains=type)
        if capacity:
            storages_list = storages_list.filter(capacity=capacity)

    # Get all Stock objects for Storages
    stock_items = Stock.objects.filter(component_type='storage')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(storages_list, 6)
    page = request.GET.get('page')
    try:
        storages = paginator.page(page)
    except PageNotAnInteger:
        storages = paginator.page(1)
    except EmptyPage:
        storages = paginator.page(paginator.num_pages)

    return render(
        request,
        'components/storage_list.html',
        {'storages': storages, 'form': form, 'stock_dict': stock_dict},
    )


def psu_list(request):
    form = PSUSearchForm(request.GET)
    psus_list = PSU.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        power = form.cleaned_data.get('power')
        certification = form.cleaned_data.get('certification')

        if q:
            psus_list = psus_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:
            psus_list = psus_list.filter(manufacturer__id__in=manufacturers)
        if power:
            psus_list = psus_list.filter(power=power)
        if certification:
            psus_list = psus_list.filter(certification__icontains=certification)

    # Get all Stock objects for PSUs
    stock_items = Stock.objects.filter(component_type='psu')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(psus_list, 6)
    page = request.GET.get('page')
    try:
        psus = paginator.page(page)
    except PageNotAnInteger:
        psus = paginator.page(1)
    except EmptyPage:
        psus = paginator.page(paginator.num_pages)

    return render(request, 'components/psu_list.html', {'psus': psus, 'form': form, 'stock_dict': stock_dict})


def case_list(request):
    form = CaseSearchForm(request.GET)
    cases_list = Case.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        form_factor = form.cleaned_data.get('form_factor')
        dimensions = form.cleaned_data.get('dimensions')
        side_panel_window = form.cleaned_data.get('side_panel_window')

        if q:
            cases_list = cases_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:
            cases_list = cases_list.filter(manufacturer__id__in=manufacturers)
        if form_factor:
            cases_list = cases_list.filter(form_factor__icontains=form_factor)
        if dimensions:
            cases_list = cases_list.filter(dimensions__icontains=dimensions)
        if side_panel_window:
            cases_list = cases_list.filter(side_panel_window=True)

    # Get all Stock objects for Cases
    stock_items = Stock.objects.filter(component_type='case')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(cases_list, 6)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)

    return render(request, 'components/case_list.html', {'cases': cases, 'form': form, 'stock_dict': stock_dict})


def cooler_list(request):
    form = CoolerSearchForm(request.GET)
    coolers_list = Cooler.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        manufacturers = form.cleaned_data.get('manufacturer')
        cooler_type = form.cleaned_data.get('cooler_type')
        fan_size = form.cleaned_data.get('fan_size')
        rgb = form.cleaned_data.get('rgb')

        if q:
            coolers_list = coolers_list.filter(
                Q(manufacturer__name__icontains=q) | Q(model__icontains=q)
            ).distinct()
        if manufacturers:  # Check if manufacturer is selected
            coolers_list = coolers_list.filter(manufacturer__id__in=manufacturers)
        if cooler_type:
            coolers_list = coolers_list.filter(cooler_type=cooler_type)
        if fan_size:
            coolers_list = coolers_list.filter(fan_size=fan_size)
        if rgb:
            coolers_list = coolers_list.filter(rgb=rgb)

    # Get all Stock objects for Coolers
    stock_items = Stock.objects.filter(component_type='cooler')
    stock_dict = {item.component_id: item for item in stock_items}

    paginator = Paginator(coolers_list, 6)
    page = request.GET.get('page')
    try:
        coolers = paginator.page(page)
    except PageNotAnInteger:
        coolers = paginator.page(1)
    except EmptyPage:
        coolers = paginator.page(paginator.num_pages)

    return render(
        request,
        'components/cooler_list.html',
        {'coolers': coolers, 'form': form, 'stock_dict': stock_dict},
    )


def cpu_detail(request, pk):
    cpu = get_object_or_404(CPU, pk=pk)
    review_form = ReviewForm()
    return render(
        request, 'components/cpu_detail.html', {'cpu': cpu, 'review_form': review_form}
    )


def gpu_detail(request, pk):
    gpu = get_object_or_404(GPU, pk=pk)
    review_form = ReviewForm()
    return render(
        request, 'components/gpu_detail.html', {'gpu': gpu, 'review_form': review_form}
    )


def motherboard_detail(request, pk):
    motherboard = get_object_or_404(Motherboard, pk=pk)
    review_form = ReviewForm()
    return render(
        request,
        'components/motherboard_detail.html',
        {'motherboard': motherboard, 'review_form': review_form},
    )


def ram_detail(request, pk):
    ram = get_object_or_404(RAM, pk=pk)
    review_form = ReviewForm()
    return render(
        request, 'components/ram_detail.html', {'ram': ram, 'review_form': review_form}
    )


def storage_detail(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    review_form = ReviewForm()
    return render(
        request,
        'components/storage_detail.html',
        {'storage': storage, 'review_form': review_form},
    )


def psu_detail(request, pk):
    psu = get_object_or_404(PSU, pk=pk)
    review_form = ReviewForm()
    return render(
        request, 'components/psu_detail.html', {'psu': psu, 'review_form': review_form}
    )


def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    review_form = ReviewForm()
    return render(
        request, 'components/case_detail.html', {'case': case, 'review_form': review_form}
    )


def cooler_detail(request, pk):
    cooler = get_object_or_404(Cooler, pk=pk)
    review_form = ReviewForm()
    return render(
        request,
        'components/cooler_detail.html',
        {'cooler': cooler, 'review_form': review_form},
    )


@login_required
def add_review(request, pk, component_type):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user

            if component_type == 'cpu':
                component = get_object_or_404(CPU, pk=pk)
            elif component_type == 'gpu':
                component = get_object_or_404(GPU, pk=pk)
            elif component_type == 'motherboard':
                component = get_object_or_404(Motherboard, pk=pk)
            elif component_type == 'ram':
                component = get_object_or_404(RAM, pk=pk)
            elif component_type == 'storage':
                component = get_object_or_404(Storage, pk=pk)
            elif component_type == 'psu':
                component = get_object_or_404(PSU, pk=pk)
            elif component_type == 'case':
                component = get_object_or_404(Case, pk=pk)
            elif component_type == 'cooler':
                component = get_object_or_404(Cooler, pk=pk)
            else:
                raise ValueError("Неверный тип компонента")

            if component:
                review.content_object = component
                review.save()
                # Construct the URL based on the component type and ID.
                return redirect(
                    reverse(
                        f'components:{component_type}_detail', kwargs={'pk': pk}
                    )
                )
            else:
                # Handle the case where no component was found.  This should ideally never happen
                # given the get_object_or_404 calls, but it's good to be defensive.
                return redirect('home')  # Or some other safe default.
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
        return redirect('home')  # Или другая подходящая страница.


def is_employee(user):  # Assuming you have this function
    return user.is_staff


@login_required
@user_passes_test(lambda u: u.is_staff)
def replenish_stock_item(request, pk):
    """Пополняет запас выбранного элемента на 10."""
    stock_item = get_object_or_404(Stock, pk=pk)
    stock_item.quantity += 10
    stock_item.save()

    # Get the out of stock count after replenishing
    out_of_stock_count = Stock.objects.filter(quantity=0).count()

    # Redirect with the out_of_stock_count as a query parameter
    url = reverse('components:stock_list') + f'?out_of_stock_count={out_of_stock_count}'
    return HttpResponseRedirect(url)


@login_required
@user_passes_test(is_employee)
def reduce_stock_item(request, pk):
    """Уменьшает запас выбранного элемента на 10."""
    stock_item = get_object_or_404(Stock, pk=pk)
    stock_item.quantity -= 10
    if stock_item.quantity < 0:
        stock_item.quantity = 0  # Предотвращаем отрицательное количество
    stock_item.save()
    return HttpResponseRedirect(reverse('components:stock_list'))


@login_required
@user_passes_test(lambda u: u.is_staff)
def stock_list_view(request):
    query = request.GET.get('q')
    stock_items = Stock.objects.all()

    if query:
        filtered_stock_items = []
        for stock_item in stock_items:
            component = None
            try:
                if stock_item.component_type == 'cpu':
                    component = CPU.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'gpu':
                    component = GPU.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'motherboard':
                    component = Motherboard.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'ram':
                    component = RAM.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'storage':
                    component = Storage.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'psu':
                    component = PSU.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'case':
                    component = Case.objects.get(pk=stock_item.component_id)
                elif stock_item.component_type == 'cooler':
                    component = Cooler.objects.get(pk=stock_item.component_id)

                if component:
                    component_name = (
                        f"{component.manufacturer} {component.model}"  # Получаем имя компонента
                    )
                    if (query.lower() in component_name.lower()) or (
                        query.lower() in str(stock_item.quantity).lower()
                    ):  # добавил поиск по quantity
                        filtered_stock_items.append(stock_item)

            except (
                CPU.DoesNotExist,
                GPU.DoesNotExist,
                Motherboard.DoesNotExist,
                RAM.DoesNotExist,
                Storage.DoesNotExist,
                PSU.DoesNotExist,
                Case.DoesNotExist,
                Cooler.DoesNotExist,
            ):
                pass  # Просто игнорируем, если компонент не найден

        stock_items = filtered_stock_items  # Заменяем stock_items отфильтрованным списком

    paginator = Paginator(stock_items, 10)
    page = request.GET.get('page')
    try:
        stock_items = paginator.get_page(page)
    except PageNotAnInteger:
        stock_items = paginator.page(1)
    except EmptyPage:
        stock_items = paginator.page(paginator.num_pages)

    # Get out of stock count
    out_of_stock_count = Stock.objects.filter(quantity=0).count()


    context = {'stock_items': stock_items, 'query': query, 'out_of_stock_count': out_of_stock_count}
    return render(request, 'builds/stock_list.html', context)