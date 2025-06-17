# components/admin.py
# components/admin.py
from django.contrib import admin
from .models import Manufacturer, CPU, GPU, Motherboard, RAM, Storage, PSU, Case, Cooler, Stock
from .forms import CPUForm, GPUForm, MotherboardForm, RAMForm, StorageForm, PSUForm, CaseForm  # Удалили Stock


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type')
    search_fields = ('name',)
    list_filter = ('component_type',)


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'cores', 'frequency', 'price', 'image')
    list_filter = ('manufacturer',)
    search_fields = ('model', 'manufacturer__name')
    ordering = ('manufacturer', 'model')
    form = CPUForm


@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'memory', 'frequency', 'tdp', 'price', 'image')
    list_filter = ('manufacturer',)
    search_fields = ('model', 'manufacturer__name')
    ordering = ('manufacturer', 'model')
    form = GPUForm


@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'form_factor', 'socket', 'chipset', 'price', 'image')
    list_filter = ('manufacturer', 'form_factor', 'socket', 'chipset')
    search_fields = ('model', 'manufacturer__name', 'socket', 'chipset')
    ordering = ('manufacturer', 'model')
    form = MotherboardForm


@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'capacity', 'frequency', 'type', 'price', 'image')
    list_filter = ('manufacturer', 'type')
    search_fields = ('model', 'manufacturer__name', 'type')
    ordering = ('manufacturer', 'model')
    form = RAMForm


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'capacity', 'type', 'interface', 'price', 'image')
    list_filter = ('manufacturer', 'type', 'interface')
    search_fields = ('model', 'manufacturer__name', 'type', 'interface')
    ordering = ('manufacturer', 'model')
    form = StorageForm


@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'power', 'certification', 'price', 'image')
    list_filter = ('manufacturer', 'certification')
    search_fields = ('model', 'manufacturer__name', 'certification')
    ordering = ('manufacturer', 'model')
    form = PSUForm


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'form_factor', 'dimensions', 'price', 'image')
    list_filter = ('manufacturer', 'form_factor')
    search_fields = ('model', 'manufacturer__name', 'form_factor')
    ordering = ('manufacturer', 'model')
    form = CaseForm


@admin.register(Cooler)
class CoolerAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'cooler_type', 'fan_size', 'price', 'image')
    list_filter = ('manufacturer', 'cooler_type')
    search_fields = ('model', 'manufacturer__name')


def replenish_stock(modeladmin, request, queryset):
    """Action для пополнения запасов."""
    for stock_item in queryset:
        stock_item.quantity += 10  # Например, пополняем на 10 штук
        stock_item.save()


replenish_stock.short_description = "Пополнить запас выбранных элементов на 10"


def reduce_stock(modeladmin, request, queryset):
    """Action для уменьшения запасов."""
    for stock_item in queryset:
        stock_item.quantity -= 10  # Например, уменьшаем на 10 штук
        stock_item.save()


reduce_stock.short_description = "Уменьшить запас выбранных элементов на 10"


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('component_type', 'get_component_name', 'quantity')
    list_filter = ('component_type',)
    search_fields = ('component_type', 'component_id')
    actions = [replenish_stock, reduce_stock]  # Добавляем actions



