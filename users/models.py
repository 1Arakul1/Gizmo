# users/models.py
from django.contrib.auth.models import User
from django.db import models

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='balance')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Баланс")
    # Можно добавить поле currency = models.CharField(max_length=3, default='RUB', verbose_name="Валюта")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return f"Баланс {self.user.username}: {self.balance}"

    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Балансы"

class Transaction(models.Model):
    """Модель для хранения истории транзакций."""
    TRANSACTION_TYPES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Снятие'),
        ('purchase', 'Покупка'),  # Добавлено для покупок в магазине
        ('refund', 'Возврат'),  # Добавлено для возвратов средств
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="Тип транзакции")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")  # Для пояснений (например, номер заказа)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.user.username} - {self.timestamp}"

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-timestamp']  # Сортировка по дате от новых к старым
