from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Stock
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CPU, GPU, Motherboard, RAM, Storage, PSU, Case, Cooler, Stock, Manufacturer


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
    return render(request, 'components/cpu_detail.html', {'cpu': cpu})


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
    return render(request, 'components/gpu_detail.html', {'gpu': gpu})


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

    return render(request, 'components/motherboard_list.html', {'motherboards': motherboards, 'form': form, 'query': query})


def motherboard_detail(request, pk):
    motherboard = get_object_or_404(Motherboard, pk=pk)
    return render(request, 'components/motherboard_detail.html', {'motherboard': motherboard})


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
    return render(request, 'components/ram_detail.html', {'ram': ram})


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
    return render(request, 'components/storage_detail.html', {'storage': storage})


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
    return render(request, 'components/psu_detail.html', {'psu': psu})


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
    return render(request, 'components/case_detail.html', {'case': case})


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
    return render(request, 'components/cooler_detail.html', {'cooler': cooler})


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
@user_passes_test(is_employee)
def stock_list_view(request):
    """
    Отображает список складских запасов для сотрудников с пагинацией и поиском.
    """
    query = request.GET.get('q')
    stock_items = Stock.objects.all()  # Начинаем с всего queryset

    if query:
        # Создаем Q-объекты для поиска по разным полям
        q_objects = Q()

        #  Проходимся по каждому элементу и ищем по нужным полям, в зависимости от типа компонента
        for stock_item in stock_items:  #  Проходимся по каждому элементу
          if stock_item.component_type == 'cpu':
            q_objects |= Q(cpu__manufacturer__icontains=query) | Q(cpu__model__icontains=query)
          elif stock_item.component_type == 'gpu':
            q_objects |= Q(gpu__manufacturer__icontains=query) | Q(gpu__model__icontains=query)
          elif stock_item.component_type == 'motherboard':
              q_objects |= Q(motherboard__manufacturer__icontains=query) | Q(motherboard__model__icontains=query)
          elif stock_item.component_type == 'ram':
              q_objects |= Q(ram__manufacturer__icontains=query) | Q(ram__model__icontains=query)
          elif stock_item.component_type == 'storage':
              q_objects |= Q(storage__manufacturer__icontains=query) | Q(storage__model__icontains=query)
          elif stock_item.component_type == 'psu':
              q_objects |= Q(psu__manufacturer__icontains=query) | Q(psu__model__icontains=query)
          elif stock_item.component_type == 'case':
              q_objects |= Q(case__manufacturer__icontains=query) | Q(case__model__icontains=query)
          elif stock_item.component_type == 'cooler':
              q_objects |= Q(cooler__manufacturer__icontains=query) | Q(cooler__model__icontains=query)
          else:
            q_objects |= Q(component_type__icontains=query)

        # Фильтруем stock_items, используя объединенные Q-объекты
        stock_items = stock_items.filter(q_objects).distinct()

    paginator = Paginator(stock_items, 10)
    page = request.GET.get('page')

    try:
        stock_items = paginator.page(page)
    except PageNotAnInteger:
        stock_items = paginator.page(1)
    except EmptyPage:
        stock_items = paginator.page(paginator.num_pages)

    response = render(request, 'builds/stock_list.html', {'stock_items': stock_items, 'query': query})
    response['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response