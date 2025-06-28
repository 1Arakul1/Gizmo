from django.contrib import admin

from .forms import (
    CPUForm,
    GPUForm,
    MotherboardForm,
    RAMForm,
    StorageForm,
    PSUForm,
    CaseForm,
    CoolerForm,
)
from .models import (
    Manufacturer,
    CPU,
    GPU,
    Motherboard,
    RAM,
    Storage,
    PSU,
    Case,
    Cooler,
    Stock,
    Review,  # Import Review
)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type')
    search_fields = ('name',)
    list_filter = ('component_type',)


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'cores',
        'frequency',
        'tdp',
        'price',
        'socket',
        'image',
        'integrated_graphics',  # Added to list display
    )
    list_filter = ('manufacturer', 'integrated_graphics')  # Added to list filter
    search_fields = ('model', 'manufacturer__name')
    ordering = ('manufacturer', 'model')
    form = CPUForm


@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'memory',
        'frequency',
        'tdp',
        'price',
        'image',
        'interface', # Added to list display
        'ray_tracing', # Added to list display
    )
    list_filter = ('manufacturer', 'ray_tracing')  # Added to list filter
    search_fields = ('model', 'manufacturer__name')
    ordering = ('manufacturer', 'model')
    form = GPUForm


@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'form_factor',
        'socket',
        'chipset',
        'price',
        'image',
        'wifi', # Added to list display
    )
    list_filter = ('manufacturer', 'form_factor', 'socket', 'chipset', 'wifi')  # Added to list filter
    search_fields = ('model', 'manufacturer__name', 'socket', 'chipset')
    ordering = ('manufacturer', 'model')
    form = MotherboardForm


@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'capacity',
        'frequency',
        'type',
        'price',
        'image',
        'rgb', # Added to list display
    )
    list_filter = ('manufacturer', 'type', 'rgb')  # Added to list filter
    search_fields = ('model', 'manufacturer__name', 'type')
    ordering = ('manufacturer', 'model')
    form = RAMForm


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'capacity',
        'type',
        'interface',
        'price',
        'image',
        'nvme', # Added to list display
    )
    list_filter = ('manufacturer', 'type', 'interface', 'nvme')  # Added to list filter
    search_fields = ('model', 'manufacturer__name', 'type', 'interface')
    ordering = ('manufacturer', 'model')
    form = StorageForm


@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'power',
        'certification',
        'price',
        'image',
        'modular', # Added to list display
    )
    list_filter = ('manufacturer', 'certification', 'modular')  # Added to list filter
    search_fields = ('model', 'manufacturer__name', 'certification')
    ordering = ('manufacturer', 'model')
    form = PSUForm


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'form_factor',
        'dimensions',
        'price',
        'image',
        'side_panel_window', # Added to list display
    )
    list_filter = ('manufacturer', 'form_factor', 'side_panel_window')  # Added to list filter
    search_fields = ('model', 'manufacturer__name', 'form_factor')
    ordering = ('manufacturer', 'model')
    form = CaseForm


@admin.register(Cooler)
class CoolerAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model',
        'cooler_type',
        'fan_size',
        'price',
        'image',
        'rgb', # Added to list display
    )
    list_filter = ('manufacturer', 'cooler_type', 'rgb')  # Added to list filter
    search_fields = ('model', 'manufacturer__name')
    form = CoolerForm


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


@admin.register(Review)  # Register the Review model
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'rating', 'content_type', 'object_id')
    list_filter = ('content_type', 'rating')
    search_fields = ('user__username', 'text')
