# components/models.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Manufacturer(models.Model):
    """Производитель компонентов."""

    name = models.CharField(max_length=255, verbose_name="Название")
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
            ('cooler', 'Охлаждение'),  # Fixed typo here
        ],
        verbose_name="Тип компонента",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class CPU(models.Model):
    """Процессор."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    cores = models.IntegerField(verbose_name="Количество ядер")
    frequency = models.FloatField(verbose_name="Частота (ГГц)")
    tdp = models.IntegerField(verbose_name="TDP (Вт)")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    socket = models.CharField(max_length=50, verbose_name="Сокет")
    image = models.ImageField(
        upload_to='cpu_images/', verbose_name="Изображение", blank=True, null=True
    )

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"
        ordering = ['manufacturer', 'model']

    def is_compatible_with_motherboard(self, motherboard):
        """Проверяет совместимость сокета процессора и материнской платы."""
        return self.socket == motherboard.socket

    reviews = GenericRelation(
        'components.Review', related_query_name='cpu'
    )  # Use string representation to avoid circular import


class Motherboard(models.Model):
    """Материнская плата."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    form_factor = models.CharField(max_length=50, verbose_name="Форм-фактор")
    socket = models.CharField(max_length=50, verbose_name="Сокет")  # Сокет процессора
    chipset = models.CharField(max_length=50, verbose_name="Чипсет")
    ram_slots = models.IntegerField(verbose_name="Слоты для RAM")
    ram_type = models.CharField(
        max_length=10, verbose_name="Тип RAM (DDR4, DDR5)"
    )
    max_ram_frequency = models.IntegerField(verbose_name="Максимальная частота RAM")
    expansion_slots = models.TextField(verbose_name="Слоты расширения")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='motherboard_images/',
        verbose_name="Изображение",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        verbose_name = "Материнская плата"
        verbose_name_plural = "Материнские платы"
        ordering = ['manufacturer', 'model']

    def is_compatible_with_cpu(self, cpu):
        """Проверяет совместимость сокета материнской платы и процессора."""
        return self.socket == cpu.socket

    def is_compatible_with_ram(self, ram):
        """Проверяет совместимость типа RAM и частоты."""
        return (
            self.ram_type == ram.type and self.max_ram_frequency >= ram.frequency
        )

    reviews = GenericRelation(
        'components.Review', related_query_name='motherboard'
    )


class RAM(models.Model):
    """Оперативная память."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    capacity = models.IntegerField(verbose_name="Объем (ГБ)")
    frequency = models.IntegerField(verbose_name="Частота (МГц)")
    type = models.CharField(max_length=10, verbose_name="Тип (DDR4, DDR5)")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='ram_images/', verbose_name="Изображение", blank=True, null=True
    )

    def __str__(self):
        return (
            f"{self.manufacturer} {self.model} ({self.capacity} ГБ, "
            f"{self.frequency} МГц)"
        )

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"
        ordering = ['manufacturer', 'model']

    def is_compatible_with_motherboard(self, motherboard):
        """Проверяет совместимость типа RAM и частоты с материнской платой."""
        return (
            self.type == motherboard.ram_type
            and self.frequency <= motherboard.max_ram_frequency
        )

    reviews = GenericRelation('components.Review', related_query_name='ram')


class GPU(models.Model):
    """Видеокарта."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    memory = models.IntegerField(verbose_name="Объем памяти (ГБ)")
    frequency = models.FloatField(verbose_name="Частота (ГГц)")  # Частота ядра
    tdp = models.IntegerField(verbose_name="TDP (Вт)")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='gpu_images/', verbose_name="Изображение", blank=True, null=True
    )
    interface = models.CharField(
        max_length=50, verbose_name="Интерфейс", default="PCIe x16"
    )  # Добавлено поле interface

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"
        ordering = ['manufacturer', 'model']

    def is_power_compatible(self, psu):
        """Проверяет, достаточно ли мощности блока питания для видеокарты."""
        return self.tdp <= psu.power

    reviews = GenericRelation('components.Review', related_query_name='gpu')


class Storage(models.Model):
    """Накопитель (SSD/HDD)."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    capacity = models.IntegerField(verbose_name="Объем (ГБ/ТБ)")
    type = models.CharField(max_length=10, verbose_name="Тип (SSD/HDD)")
    interface = models.CharField(max_length=50, verbose_name="Интерфейс")
    read_speed = models.IntegerField(verbose_name="Скорость чтения (МБ/с)")
    write_speed = models.IntegerField(verbose_name="Скорость записи (МБ/с)")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='storage_images/',
        verbose_name="Изображение",
        blank=True,
        null=True,
    )

    def __str__(self):
        return (
            f"{self.manufacturer} {self.model} ({self.capacity} ГБ, "
            f"{self.type})"
        )

    class Meta:
        verbose_name = "Накопитель"
        verbose_name_plural = "Накопители"
        ordering = ['manufacturer', 'model']

    reviews = GenericRelation('components.Review', related_query_name='storage')


class PSU(models.Model):
    """Блок питания."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    power = models.IntegerField(verbose_name="Мощность (Вт)")
    certification = models.CharField(max_length=50, verbose_name="Сертификация")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='psu_images/', verbose_name="Изображение", blank=True, null=True
    )

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.power} Вт)"

    class Meta:
        verbose_name = "Блок питания"
        verbose_name_plural = "Блоки питания"
        ordering = ['manufacturer', 'model']

    def is_sufficient_for_gpu(self, gpu):
        """Проверяет, достаточно ли мощности блока питания для видеокарты."""
        return self.power >= gpu.tdp

    reviews = GenericRelation('components.Review', related_query_name='psu')


class Case(models.Model):
    """Корпус."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    form_factor = models.CharField(max_length=50, verbose_name="Форм-фактор")
    dimensions = models.CharField(max_length=50, verbose_name="Размеры")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='case_images/', verbose_name="Изображение", blank=True, null=True
    )
    supported_motherboard_form_factors = models.CharField(
        max_length=255,
        verbose_name="Поддерживаемые форм-факторы мат. плат",
        default="ATX, Micro-ATX, Mini-ITX",
    )

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.form_factor})"

    class Meta:
        verbose_name = "Корпус"
        verbose_name_plural = "Корпуса"
        ordering = ['manufacturer', 'model']

    reviews = GenericRelation('components.Review', related_query_name='case')


class Build(models.Model):
    """Сборка компьютера."""

    name = models.CharField(
        max_length=255,
        verbose_name="Название сборки",
        blank=True,
        null=True,
    )  # Добавил поле название сборки
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.CASCADE,
        verbose_name="Процессор",
        related_name='builds',
    )
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.CASCADE,
        verbose_name="Материнская плата",
        blank=True,
        null=True,
        related_name='builds',
    )
    ram = models.ForeignKey(
        RAM,
        on_delete=models.CASCADE,
        verbose_name="Оперативная память",
        blank=True,
        null=True,
        related_name='builds',
    )
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.CASCADE,
        verbose_name="Видеокарта",
        blank=True,
        null=True,
        related_name='builds',
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name="Накопитель",
        blank=True,
        null=True,
        related_name='builds',
    )
    psu = models.ForeignKey(
        PSU,
        on_delete=models.CASCADE,
        verbose_name="Блок питания",
        blank=True,
        null=True,
        related_name='builds',
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        verbose_name="Корпус",
        blank=True,
        null=True,
        related_name='builds',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='builds',
        blank=True,
        null=True,
    )

    def __str__(self):
        return (
            f"Сборка {self.pk} - {self.name if self.name else 'Без имени'}"
        )

    @admin.display(description='Общая стоимость')
    def get_total_price(self):
        """Вычисляет общую стоимость сборки."""
        price = 0.0
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
        return price

    class Meta:
        verbose_name = "Сборка"
        verbose_name_plural = "Сборки"
        ordering = ['name']


class Cooler(models.Model):
    """Охлаждение (кулер для CPU)."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")
    cooler_type = models.CharField(
        max_length=50,
        verbose_name="Тип охлаждения",
        choices=[
            ('air', 'Воздушное'),
            ('liquid', 'Жидкостное'),
        ],
    )
    fan_size = models.IntegerField(
        verbose_name="Размер вентилятора (мм)", blank=True, null=True
    )  # Только для воздушных
    radiator_size = models.CharField(
        max_length=50,
        verbose_name="Размер радиатора",
        blank=True,
        null=True,
    )  # Только для жидкостных
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField(
        upload_to='cooler_images/', verbose_name="Изображение", blank=True, null=True
    )

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        verbose_name = "Охлаждение"
        verbose_name_plural = "Охлаждения"
        ordering = ['manufacturer', 'model']

    def is_compatible_with_cpu(self, cpu):
        """Проверяет совместимость с CPU."""
        # Добавьте логику проверки (например, сокет, TDP и т.д.)
        return True  # Заглушка

    reviews = GenericRelation('components.Review', related_query_name='cooler')


class Stock(models.Model):
    """Модель для учета складских запасов компонентов."""

    COMPONENT_TYPE_CHOICES = [
        ('cpu', 'Процессор'),
        ('gpu', 'Видеокарта'),
        ('motherboard', 'Материнская плата'),
        ('ram', 'Оперативная память'),
        ('storage', 'Накопитель'),
        ('psu', 'Блок питания'),
        ('case', 'Корпус'),
        ('cooler', 'Охлаждение'),
    ]

    component_type = models.CharField(
        max_length=50,
        choices=COMPONENT_TYPE_CHOICES,
        verbose_name="Тип компонента",
    )
    component_id = models.PositiveIntegerField(verbose_name="ID компонента")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return f"{self.get_component_name()} - {self.quantity}"

    def get_component_name(self):
        """Возвращает имя компонента."""
        component_model = {
            'cpu': CPU,
            'gpu': GPU,
            'motherboard': Motherboard,
            'ram': RAM,
            'storage': Storage,
            'psu': PSU,
            'case': Case,
            'cooler': Cooler,
        }.get(self.component_type)

        if component_model:
            try:
                component = component_model.objects.get(pk=self.component_id)
                return f"{component.manufacturer} {component.model}"
            except component_model.DoesNotExist:
                return "Компонент не найден"
        else:
            return "Неизвестный тип компонента"

    def get_component_type_display(self):
        return dict(self.COMPONENT_TYPE_CHOICES).get(
            self.component_type, 'Unknown'
        )

    class Meta:
        verbose_name = "Складской запас"
        verbose_name_plural = "Складские запасы"
        unique_together = (
            'component_type',
            'component_id',
        )  # Гарантирует уникальность записи для каждого компонен


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(1, "1 звезда"), (2, "2 звезды"), (3, "3 звезды"), (4, "4 звезды"),
                                           (5, "5 звезд")], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    # Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.content_object}"
