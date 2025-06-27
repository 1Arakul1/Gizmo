# builds/models.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
import uuid

from components.models import (
    CPU,
    GPU,
    Motherboard,
    RAM,
    Storage,
    PSU,
    Case,
    Cooler,
)


class Build(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.SET_NULL,
        verbose_name="CPU",
        blank=True,
        null=True,
    )
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.SET_NULL,
        verbose_name="GPU",
        blank=True,
        null=True,
    )
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.SET_NULL,
        verbose_name="Motherboard",
        blank=True,
        null=True,
    )
    ram = models.ForeignKey(
        RAM,
        on_delete=models.SET_NULL,
        verbose_name="RAM",
        blank=True,
        null=True,
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.SET_NULL,
        verbose_name="Storage",
        blank=True,
        null=True,
    )
    psu = models.ForeignKey(
        PSU,
        on_delete=models.SET_NULL,
        verbose_name="PSU",
        blank=True,
        null=True,
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.SET_NULL,
        verbose_name="Case",
        blank=True,
        null=True,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость",
        blank=True,
        null=True,
    )
    cooler = models.ForeignKey(
        Cooler,
        on_delete=models.SET_NULL,
        verbose_name="Охлаждение",
        blank=True,
        null=True,
        related_name='builds',
    )

    def __str__(self):
        return (
            f"Сборка {self.pk} - {self.cpu.model if self.cpu else 'Без CPU'}"
        )

    @admin.display(description='Общая стоимость')
    def get_total_price(self):
        price = 0
        if self.cpu:
            price += self.cpu.price
        if self.gpu:
            price += self.gpu.price
        if self.motherboard:
            price += self.motherboard.price
        if self.ram:
            price += self.ram.price
        if self.storage:
            price += self.storage.price
        if self.psu:
            price += self.psu.price
        if self.case:
            price += self.case.price
        if self.cooler:
            price += self.cooler.price
        return price

    class Meta:
        verbose_name = "Сборка"
        verbose_name_plural = "Сборки"


class CartItem(models.Model):
    """Элемент в корзине."""

    build = models.ForeignKey(
        'Build',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Сборка",
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.CASCADE,
        verbose_name="Процессор",
        blank=True,
        null=True,
    )
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.CASCADE,
        verbose_name="Видеокарта",
        blank=True,
        null=True,
    )
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.CASCADE,
        verbose_name="Материнская плата",
        blank=True,
        null=True,
    )
    ram = models.ForeignKey(
        RAM,
        on_delete=models.CASCADE,
        verbose_name="Оперативная память",
        blank=True,
        null=True,
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name="Накопитель",
        blank=True,
        null=True,
    )
    psu = models.ForeignKey(
        PSU,
        on_delete=models.CASCADE,
        verbose_name="Блок питания",
        blank=True,
        null=True,
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        verbose_name="Корпус",
        blank=True,
        null=True,
    )
    cooler = models.ForeignKey(
        Cooler,
        on_delete=models.CASCADE,
        verbose_name="Охлаждение",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.build:
            return (
                f"Сборка {self.build.pk} в корзине для "
                f"{self.user.username}"
            )
        elif self.cpu:
            return (
                f"CPU {self.cpu.manufacturer} {self.cpu.model} для "
                f"{self.user.username}"
            )
        elif self.gpu:
            return (
                f"GPU {self.gpu.manufacturer} {self.gpu.model} для "
                f"{self.user.username}"
            )
        elif self.motherboard:
            return (
                f"Motherboard {self.motherboard.manufacturer} "
                f"{self.motherboard.model} для {self.user.username}"
            )
        elif self.ram:
            return (
                f"RAM {self.ram.manufacturer} {self.ram.model} для "
                f"{self.user.username}"
            )
        elif self.storage:
            return (
                f"Storage {self.storage.manufacturer} {self.storage.model} для "
                f"{self.user.username}"
            )
        elif self.psu:
            return (
                f"PSU {self.psu.manufacturer} {self.psu.model} для "
                f"{self.user.username}"
            )
        elif self.case:
            return (
                f"Case {self.case.manufacturer} {self.case.model} для "
                f"{self.user.username}"
            )
        elif self.cooler:
            return (
                f"Cooler {self.cooler.manufacturer} {self.cooler.model} для "
                f"{self.user.username}"
            )
        else:
            return (
                f"Неизвестный товар в корзине для {self.user.username}"
            )

    def get_total_price(self):
        price = 0
        if self.build:
            price = self.build.total_price
        elif self.cpu:
            price = self.cpu.price
        elif self.gpu:
            price = self.gpu.price
        elif self.motherboard:
            price = self.motherboard.price
        elif self.ram:
            price = self.ram.price
        elif self.storage:
            price = self.storage.price
        elif self.psu:
            price = self.psu.price
        elif self.case:
            price = self.case.price
        elif self.cooler:
            price = self.cooler.price
        return price * self.quantity

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"


class Order(models.Model):
    """Модель для хранения информации о заказе."""

    STATUS_CHOICES = [
        ('pending', 'Заказ на рассмотрении'),
        ('confirmed', 'Заказ подтверждён'),
        ('assembling', 'Заказ собирается'),
        ('delivery_prep', 'Заказ готовится к доставке'),
        ('delivering', 'Заказ будет доставлен вам в течении 3 часов'),
        ('delivered', 'Заказ доставлен, заберите его'),
        ('completed', 'Заказ выполнен'),
    ]

    DELIVERY_OPTIONS = [
        ('pickup', 'Самовывоз из магазина'),
        ('courier', 'Доставка курьером'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    email = models.EmailField(verbose_name="Email")
    delivery_option = models.CharField(
        max_length=50,
        verbose_name="Способ доставки",
        choices=DELIVERY_OPTIONS,
    )
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес доставки",
        blank=True,
        null=True,
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая сумма"
    )
    order_date = models.DateTimeField(verbose_name="Дата заказа")
    track_number = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Трек-номер",
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа",
    )
    is_completed = models.BooleanField(
        default=False, verbose_name="Заказ выдан"
    )

    # Добавляем поле для связи с запросом на возврат
    return_request = models.OneToOneField(
        'ReturnRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Запрос на возврат",
        related_name='order',
    )

    def save(self, *args, **kwargs):
        if not self.track_number:
            self.track_number = self.generate_track_number()
        super().save(*args, **kwargs)

    def generate_track_number(self):
        """Генерирует уникальный 8-значный трек-номер."""
        return str(uuid.uuid4().hex)[:8].upper()

    def __str__(self):
        return (
            f"Заказ #{self.pk} - {self.user.username} - "
            f"{self.track_number} ({self.status})"
        )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-order_date']


class OrderItem(models.Model):
    """Модель для хранения позиций заказа."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Заказ"
    )
    item = models.CharField(max_length=255, verbose_name="Наименование товара")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    component_type = models.CharField(
        max_length=50,
        choices=[
            ('cpu', 'Процессор'),
            ('gpu', 'Видеокарта'),
            ('motherboard', 'Материнская плата'),
            ('ram', 'Оперативная память'),
            ('storage', 'Накопитель'),
            ('psu', 'Блок питания'),
            ('case', 'Корпус'),
            ('cooler', 'Охлаждение'),
        ],
        verbose_name="Тип компонента",
        blank=True,
        null=True,
    )
    component_id = models.PositiveIntegerField(
        verbose_name="ID компонента", blank=True, null=True
    )

    def __str__(self):
        return f"{self.item} x {self.quantity} в заказе #{self.order.pk}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"


class ReturnRequest(models.Model):
    """Модель для запросов на возврат товара."""

    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен'),
        ('returned', 'Возвращен'),
        ('refunded', 'Возмещены средства'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    order_item = models.ForeignKey(
        'OrderItem',
        on_delete=models.CASCADE,
        verbose_name="Позиция заказа",
    )  # Связываем с конкретной позицией заказа
    reason = models.TextField(verbose_name="Причина возврата")
    request_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата запроса"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус запроса",
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий сотрудника",
    )  # Комментарий сотрудника при рассмотрении

    def __str__(self):
        return (
            f"Запрос на возврат #{self.pk} от "
            f"{self.user.username} - {self.order_item.item}"
        )

    class Meta:
        verbose_name = "Запрос на возврат"
        verbose_name_plural = "Запросы на возврат"
        ordering = ['-request_date']
