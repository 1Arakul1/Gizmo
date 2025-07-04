# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Balance, Transaction  # Импортируем модели Balance и Transaction

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'last_update')
    search_fields = ('user__username', 'user__email')  # Поиск по имени пользователя и email

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('user__username', 'user__email')

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Balance, BalanceAdmin)  # Регистрируем модель Balance с настройками
admin.site.register(Transaction, TransactionAdmin)  # Регистрируем модель Transaction с настройками
