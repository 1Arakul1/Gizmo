# builds/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Build, Order, OrderItem  # CartItem больше не импортируется


class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            ('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )



admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class OrderItemInline(admin.TabularInline):  # Или admin.StackedInline
    model = OrderItem
    extra = 0  # Убирает лишние пустые формы
    readonly_fields = ('item', 'quantity', 'price')
    can_delete = False

    def has_add_permission(self, request, obj):
        return False  # Запрещаем добавление новых элементов inline


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'email',
        'order_date',
        'status',
        'track_number',
        'total_amount',
    )
    list_filter = ('status', 'order_date', 'user')
    search_fields = ('track_number', 'email', 'user__username')
    date_hierarchy = 'order_date'
    inlines = [OrderItemInline]
    readonly_fields = (
        'track_number',
        'order_date',
        'user',
        'email',
        'delivery_option',
        'payment_method',
        'address',
        'total_amount',
    )
    list_editable = ('status',)
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'user',
                'email',
                'delivery_option',
                'payment_method',
                'address',
                'total_amount',
                'order_date',
                'track_number',
            )
        }),
        ('Статус заказа', {'fields': ('status',)}),
    )

    def has_add_permission(self, request):
        return False


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'cpu', 'gpu', 'total_price')
    list_filter = ('user', 'cpu__manufacturer', 'gpu__manufacturer')
    search_fields = ('user__username', 'cpu__model', 'gpu__model')
    readonly_fields = ('total_price',)
