# builds/models.py
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
    """Модель для представления сборки компьютера."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )  # Связь с моделью пользователя.  При удалении пользователя удаляются все его сборки.
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.SET_NULL,
        verbose_name="CPU",
        blank=True,
        null=True,
    )  # Связь с моделью процессора. Если процессор удален, поле становится NULL.
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.SET_NULL,
        verbose_name="GPU",
        blank=True,
        null=True,
    )  # Связь с моделью видеокарты. Если видеокарта удалена, поле становится NULL.
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.SET_NULL,
        verbose_name="Motherboard",
        blank=True,
        null=True,
    )  # Связь с моделью материнской платы. Если материнская плата удалена, поле становится NULL.
    ram = models.ForeignKey(
        RAM,
        on_delete=models.SET_NULL,
        verbose_name="RAM",
        blank=True,
        null=True,
    )  # Связь с моделью оперативной памяти. Если оперативная память удалена, поле становится NULL.
    storage = models.ForeignKey(
        Storage,
        on_delete=models.SET_NULL,
        verbose_name="Storage",
        blank=True,
        null=True,
    )  # Связь с моделью накопителя. Если накопитель удален, поле становится NULL.
    psu = models.ForeignKey(
        PSU,
        on_delete=models.SET_NULL,
        verbose_name="PSU",
        blank=True,
        null=True,
    )  # Связь с моделью блока питания. Если блок питания удален, поле становится NULL.
    case = models.ForeignKey(
        Case,
        on_delete=models.SET_NULL,
        verbose_name="Case",
        blank=True,
        null=True,
    )  # Связь с моделью корпуса. Если корпус удален, поле становится NULL.
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость",
        blank=True,
        null=True,
    )  # Общая стоимость сборки.  Может быть рассчитана автоматически.
    cooler = models.ForeignKey(
        Cooler,
        on_delete=models.SET_NULL,
        verbose_name="Охлаждение",
        blank=True,
        null=True,
        related_name='builds',
    )  # Связь с моделью системы охлаждения. Если охлаждение удалено, поле становится NULL.  `related_name='builds'` позволяет получить доступ к сборкам из модели Cooler.

    def __str__(self):
        """Строковое представление объекта сборки."""
        return (
            f"Сборка {self.pk} - {self.cpu.model if self.cpu else 'Без CPU'}"
        )  # Возвращает строку, содержащую ID сборки и модель процессора (если он есть).

    @admin.display(description='Общая стоимость')
    def get_total_price(self):
        """Вычисляет и возвращает общую стоимость сборки."""
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
        return price  # Возвращает общую стоимость сборки.

    class Meta:
        """Метаданные модели сборки."""

        verbose_name = "Сборка"  # Название модели в единственном числе.
        verbose_name_plural = "Сборки"  # Название модели во множественном числе.


class CartItem(models.Model):
    """Элемент в корзине."""

    build = models.ForeignKey(
        'Build',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Сборка",
    )  # Связь с моделью сборки. Если сборка удалена, элемент корзины тоже удаляется.
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество"
    )  # Количество данного элемента в корзине.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )  # Связь с моделью пользователя. При удалении пользователя удаляются все его элементы корзины.
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.CASCADE,
        verbose_name="Процессор",
        blank=True,
        null=True,
    )  # Связь с моделью процессора. Если процессор удален, элемент корзины тоже удаляется.
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.CASCADE,
        verbose_name="Видеокарта",
        blank=True,
        null=True,
    )  # Связь с моделью видеокарты. Если видеокарта удалена, элемент корзины тоже удаляется.
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.CASCADE,
        verbose_name="Материнская плата",
        blank=True,
        null=True,
    )  # Связь с моделью материнской платы. Если материнская плата удалена, элемент корзины тоже удаляется.
    ram = models.ForeignKey(
        RAM,
        on_delete=models.CASCADE,
        verbose_name="Оперативная память",
        blank=True,
        null=True,
    )  # Связь с моделью оперативной памяти. Если оперативная память удалена, элемент корзины тоже удаляется.
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name="Накопитель",
        blank=True,
        null=True,
    )  # Связь с моделью накопителя. Если накопитель удален, элемент корзины тоже удаляется.
    psu = models.ForeignKey(
        PSU,
        on_delete=models.CASCADE,
        verbose_name="Блок питания",
        blank=True,
        null=True,
    )  # Связь с моделью блока питания. Если блок питания удален, элемент корзины тоже удаляется.
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        verbose_name="Корпус",
        blank=True,
        null=True,
    )  # Связь с моделью корпуса. Если корпус удален, элемент корзины тоже удаляется.
    cooler = models.ForeignKey(
        Cooler,
        on_delete=models.CASCADE,
        verbose_name="Охлаждение",
        blank=True,
        null=True,
    )  # Связь с моделью системы охлаждения. Если система охлаждения удалена, элемент корзины тоже удаляется.

    def __str__(self):
        """Строковое представление элемента корзины."""
        if self.build:
            return (
                f"Сборка {self.build.pk} в корзине для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине сборка.
        elif self.cpu:
            return (
                f"CPU {self.cpu.manufacturer} {self.cpu.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине процессор.
        elif self.gpu:
            return (
                f"GPU {self.gpu.manufacturer} {self.gpu.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине видеокарта.
        elif self.motherboard:
            return (
                f"Motherboard {self.motherboard.manufacturer} "
                f"{self.motherboard.model} для {self.user.username}"
            )  # Возвращает строку, если в корзине материнская плата.
        elif self.ram:
            return (
                f"RAM {self.ram.manufacturer} {self.ram.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине оперативная память.
        elif self.storage:
            return (
                f"Storage {self.storage.manufacturer} {self.storage.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине накопитель.
        elif self.psu:
            return (
                f"PSU {self.psu.manufacturer} {self.psu.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине блок питания.
        elif self.case:
            return (
                f"Case {self.case.manufacturer} {self.case.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине корпус.
        elif self.cooler:
            return (
                f"Cooler {self.cooler.manufacturer} {self.cooler.model} для "
                f"{self.user.username}"
            )  # Возвращает строку, если в корзине система охлаждения.
        else:
            return (
                f"Неизвестный товар в корзине для {self.user.username}"
            )  # Возвращает строку, если тип товара в корзине неизвестен.

    def get_total_price(self):
        """Вычисляет и возвращает общую стоимость элемента корзины с учетом количества."""
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
        return price * self.quantity  # Возвращает общую стоимость элемента корзины (цена * количество).

    class Meta:
        """Метаданные модели элемента корзины."""

        verbose_name = "Элемент корзины"  # Название модели в единственном числе.
        verbose_name_plural = "Элементы корзины"  # Название модели во множественном числе.


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
    ]  # Возможные статусы заказа.

    DELIVERY_OPTIONS = [
        ('pickup', 'Самовывоз из магазина'),
        ('courier', 'Доставка курьером'),
    ]  # Возможные способы доставки.

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )  # Связь с моделью пользователя. При удалении пользователя удаляются все его заказы.
    email = models.EmailField(verbose_name="Email")  # Email пользователя для связи.
    delivery_option = models.CharField(
        max_length=50,
        verbose_name="Способ доставки",
        choices=DELIVERY_OPTIONS,
    )  # Выбранный способ доставки.
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")  # Выбранный способ оплаты.
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес доставки",
        blank=True,
        null=True,
    )  # Адрес доставки (если выбран способ доставки "курьером").
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая сумма"
    )  # Общая сумма заказа.
    order_date = models.DateTimeField(verbose_name="Дата заказа")  # Дата оформления заказа.
    track_number = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Трек-номер",
        db_index=True,
    )  # Уникальный трек-номер для отслеживания заказа.  Индексирован для быстрого поиска.
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа",
    )  # Текущий статус заказа.
    is_completed = models.BooleanField(
        default=False, verbose_name="Заказ выдан"
    )  # Флаг, указывающий, был ли заказ выдан/завершен.

    # Добавляем поле для связи с запросом на возврат
    return_request = models.OneToOneField(
        'ReturnRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Запрос на возврат",
        related_name='order',
    )  # Связь с моделью запроса на возврат. Если запрос на возврат удален, поле становится NULL. OneToOneField обеспечивает связь только с одним запросом на возврат. related_name='order' позволяет получить доступ к заказу из модели ReturnRequest.

    def save(self, *args, **kwargs):
        """Переопределенный метод save() для автоматической генерации трек-номера перед сохранением."""
        if not self.track_number:
            self.track_number = self.generate_track_number()  # Генерируем трек-номер, если он еще не задан.
        super().save(*args, **kwargs)  # Вызываем стандартный метод save() для сохранения объекта.

    def generate_track_number(self):
        """Генерирует уникальный 8-значный трек-номер."""
        return str(uuid.uuid4().hex)[:8].upper()  # Генерируем случайный UUID, берем первые 8 символов и приводим к верхнему регистру.

    def __str__(self):
        """Строковое представление объекта заказа."""
        return (
            f"Заказ #{self.pk} - {self.user.username} - "
            f"{self.track_number} ({self.status})"
        )  # Возвращает строку, содержащую ID заказа, имя пользователя, трек-номер и статус.

    class Meta:
        """Метаданные модели заказа."""

        verbose_name = "Заказ"  # Название модели в единственном числе.
        verbose_name_plural = "Заказы"  # Название модели во множественном числе.
        ordering = ['-order_date']  # Сортировка заказов по дате в обратном порядке (от новых к старым).


class OrderItem(models.Model):
    """Модель для хранения позиций заказа."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Заказ"
    )  # Связь с моделью заказа. Если заказ удален, удаляются все его позиции.
    item = models.CharField(max_length=255, verbose_name="Наименование товара")  # Наименование товара в заказе.
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")  # Количество товара в заказе.
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )  # Цена товара в заказе на момент оформления.
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
    )  # Тип компонента, если позиция заказа является компонентом.
    component_id = models.PositiveIntegerField(
        verbose_name="ID компонента", blank=True, null=True
    )  # ID компонента, если позиция заказа является компонентом.

    def __str__(self):
        """Строковое представление позиции заказа."""
        return f"{self.item} x {self.quantity} в заказе #{self.order.pk}"  # Возвращает строку, содержащую наименование товара, количество и ID заказа.

    class Meta:
        """Метаданные модели позиции заказа."""

        verbose_name = "Позиция заказа"  # Название модели в единственном числе.
        verbose_name_plural = "Позиции заказа"  # Название модели во множественном числе.


class ReturnRequest(models.Model):
    """Модель для запросов на возврат товара."""

    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен'),
        ('returned', 'Возвращен'),
        ('refunded', 'Возмещены средства'),
    ]  # Возможные статусы запроса на возврат.

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )  # Связь с моделью пользователя. При удалении пользователя удаляются все его запросы на возврат.
    order_item = models.ForeignKey(
        'OrderItem',
        on_delete=models.CASCADE,
        verbose_name="Позиция заказа",
    )  # Связываем с конкретной позицией заказа. Если позиция заказа удалена, запрос на возврат тоже удаляется.
    reason = models.TextField(verbose_name="Причина возврата")  # Причина возврата, указанная пользователем.
    request_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата запроса"
    )  # Дата создания запроса на возврат.  auto_now_add=True: поле автоматически устанавливается в текущее время при создании объекта.
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус запроса",
    )  # Текущий статус запроса на возврат.
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий сотрудника",
    )  # Комментарий сотрудника при рассмотрении запроса на возврат.

    def __str__(self):
        """Строковое представление запроса на возврат."""
        return (
            f"Запрос на возврат #{self.pk} от "
            f"{self.user.username} - {self.order_item.item}"
        )  # Возвращает строку, содержащую ID запроса, имя пользователя и наименование товара из позиции заказа.

    class Meta:
        """Метаданные модели запроса на возврат."""

        verbose_name = "Запрос на возврат"  # Название модели в единственном числе.
        verbose_name_plural = "Запросы на возврат"  # Название модели во множественном числе.
        ordering = ['-request_date']  # Сортировка запросов на возврат по дате в обратном порядке (от новых к старым).
