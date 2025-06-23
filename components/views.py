from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CPU, GPU, Motherboard, RAM, Storage, PSU, Case, Cooler, Stock, Manufacturer
from .forms import ReviewForm
from django.contrib.contenttypes.models import ContentType  # Correct import


class ComponentSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)


def cpu_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    cpus_list = CPU.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            cpus_list = cpus_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(cpus_list, 6)
    page = request.GET.get('page')
    try:
        cpus = paginator.page(page)
    except PageNotAnInteger:
        cpus = paginator.page(1)
    except EmptyPage:
        cpus = paginator.page(paginator.num_pages)

    return render(request, 'components/cpu_list.html', {'cpus': cpus, 'form': form, 'query': query})


def cpu_detail(request, pk):
    cpu = get_object_or_404(CPU, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/cpu_detail.html', {'cpu': cpu, 'review_form': review_form})


def gpu_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    gpus_list = GPU.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            gpus_list = gpus_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(gpus_list, 6)
    page = request.GET.get('page')
    try:
        gpus = paginator.page(page)
    except PageNotAnInteger:
        gpus = paginator.page(1)
    except EmptyPage:
        gpus = paginator.page(paginator.num_pages)

    return render(request, 'components/gpu_list.html', {'gpus': gpus, 'form': form, 'query': query})


def gpu_detail(request, pk):
    gpu = get_object_or_404(GPU, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/gpu_detail.html', {'gpu': gpu, 'review_form': review_form})


def motherboard_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    motherboards_list = Motherboard.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            motherboards_list = motherboards_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(motherboards_list, 6)
    page = request.GET.get('page')
    try:
        motherboards = paginator.page(page)
    except PageNotAnInteger:
        motherboards = paginator.page(1)
    except EmptyPage:
        motherboards = paginator.page(paginator.num_pages)

    return render(request, 'components/motherboard_list.html',
                  {'motherboards': motherboards, 'form': form, 'query': query})


def motherboard_detail(request, pk):
    motherboard = get_object_or_404(Motherboard, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/motherboard_detail.html', {'motherboard': motherboard, 'review_form': review_form})


def ram_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    rams_list = RAM.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            rams_list = rams_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(rams_list, 6)
    page = request.GET.get('page')
    try:
        rams = paginator.page(page)
    except PageNotAnInteger:
        rams = paginator.page(1)
    except EmptyPage:
        rams = paginator.page(paginator.num_pages)

    return render(request, 'components/ram_list.html', {'rams': rams, 'form': form, 'query': query})


def ram_detail(request, pk):
    ram = get_object_or_404(RAM, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/ram_detail.html', {'ram': ram, 'review_form': review_form})


def storage_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    storages_list = Storage.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            storages_list = storages_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(storages_list, 6)
    page = request.GET.get('page')
    try:
        storages = paginator.page(page)
    except PageNotAnInteger:
        storages = paginator.page(1)
    except EmptyPage:
        storages = paginator.page(paginator.num_pages)

    return render(request, 'components/storage_list.html', {'storages': storages, 'form': form, 'query': query})


def storage_detail(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/storage_detail.html', {'storage': storage, 'review_form': review_form})


def psu_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    psus_list = PSU.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            psus_list = psus_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(psus_list, 6)
    page = request.GET.get('page')
    try:
        psus = paginator.page(page)
    except PageNotAnInteger:
        psus = paginator.page(1)
    except EmptyPage:
        psus = paginator.page(paginator.num_pages)

    return render(request, 'components/psu_list.html', {'psus': psus, 'form': form, 'query': query})


def psu_detail(request, pk):
    psu = get_object_or_404(PSU, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/psu_detail.html', {'psu': psu, 'review_form': review_form})


def case_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    cases_list = Case.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            cases_list = cases_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(cases_list, 6)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)

    return render(request, 'components/case_list.html', {'cases': cases, 'form': form, 'query': query})


def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/case_detail.html', {'case': case, 'review_form': review_form})


def cooler_list(request):
    form = ComponentSearchForm(request.GET)
    query = ''
    coolers_list = Cooler.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            coolers_list = coolers_list.filter(
                Q(manufacturer__name__icontains=query) | Q(model__icontains=query)
            ).distinct()

    paginator = Paginator(coolers_list, 6)
    page = request.GET.get('page')
    try:
        coolers = paginator.page(page)
    except PageNotAnInteger:
        coolers = paginator.page(1)
    except EmptyPage:
        coolers = paginator.page(paginator.num_pages)

    return render(request, 'components/cooler_list.html', {'coolers': coolers, 'form': form, 'query': query})


def cooler_detail(request, pk):
    cooler = get_object_or_404(Cooler, pk=pk)
    review_form = ReviewForm()
    return render(request, 'components/cooler_detail.html', {'cooler': cooler, 'review_form': review_form})


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
                return redirect(reverse(f'components:{component_type}_detail', kwargs={'pk': pk}))
            else:
                # Handle the case where no component was found.  This should ideally never happen
                # given the get_object_or_404 calls, but it's good to be defensive.
                return redirect('home') # Or some other safe default.
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
        return redirect('home') # Или другая подходящая страница.



def is_employee(user):  # Assuming you have this function
    return user.is_staff


@login_required
@user_passes_test(is_employee)
def replenish_stock_item(request, pk):
    """Пополняет запас выбранного элемента на 10."""
    stock_item = get_object_or_404(Stock, pk=pk)
    stock_item.quantity += 10
    stock_item.save()
    return HttpResponseRedirect(reverse('components:stock_list'))


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
                    component_name = f"{component.manufacturer} {component.model}"  # Получаем имя компонента
                    if (query.lower() in component_name.lower()) or \
                       (query.lower() in str(stock_item.quantity).lower()): # добавил поиск по quantity
                        filtered_stock_items.append(stock_item)

            except (CPU.DoesNotExist, GPU.DoesNotExist, Motherboard.DoesNotExist, RAM.DoesNotExist,
                    Storage.DoesNotExist, PSU.DoesNotExist, Case.DoesNotExist, Cooler.DoesNotExist):
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

    context = {'stock_items': stock_items, 'query': query}
    return render(request, 'builds/stock_list.html', context)