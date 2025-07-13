# components/models.py
from django.contrib import admin  # Импортирует модуль admin для настройки административного интерфейса Django.
from django.contrib.auth import get_user_model  # Импортирует функцию для получения текущей модели пользователя Django.
from django.contrib.contenttypes.fields import (  # Импортирует поля для реализации Generic Relations (обобщенных связей).
    GenericForeignKey,  # Поле, которое позволяет связать модель с объектом любой другой модели.
    GenericRelation,  # Поле, которое позволяет связать несколько объектов другой модели с данной моделью.
)
from django.contrib.contenttypes.models import ContentType  # Импортирует модель ContentType для хранения информации о моделях.
from django.core.validators import MinValueValidator  # Импортирует валидатор для проверки минимального значения поля.
from django.db import models  # Импортирует модуль models для определения моделей базы данных.

User = get_user_model()  # Получает модель пользователя, используемую в проекте.

# Определение модели Manufacturer (Производитель)
class Manufacturer(models.Model):
    """Производитель компонентов."""

    name = models.CharField(max_length=255, verbose_name="Название")  # Название производителя (строка, максимум 255 символов).
    component_type = models.CharField(  # Тип компонента, производимого данным производителем.
        max_length=50,
        choices=[  # Возможные значения типа компонента.
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
        blank=True,  # Поле может быть пустым.
        null=True,  # Поле может быть None (NULL в базе данных).
    )

    def __str__(self):
        return self.name  # Возвращает название производителя при преобразовании объекта в строку.

    class Meta:
        verbose_name = "Производитель"  # Название модели в единственном числе для административного интерфейса.
        verbose_name_plural = "Производители"  # Название модели во множественном числе для административного интерфейса.


# Определение модели CPU (Процессор)
class CPU(models.Model):
    """Процессор."""

    manufacturer = models.ForeignKey(  # Связь "один ко многим" с моделью Manufacturer.
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель" # Если производитель удален, все связанные процессоры тоже удаляются (CASCADE).
    )
    model = models.CharField(max_length=255, verbose_name="Модель")  # Модель процессора (строка, максимум 255 символов).
    cores = models.IntegerField(verbose_name="Количество ядер")  # Количество ядер процессора (целое число).
    frequency = models.FloatField(verbose_name="Частота (ГГц)")  # Частота процессора (число с плавающей точкой).
    tdp = models.IntegerField(verbose_name="TDP (Вт)")  # TDP (Thermal Design Power) процессора (целое число).
    price = models.DecimalField(  # Цена процессора (число с фиксированной точностью).
        max_digits=10,  # Максимальное количество цифр.
        decimal_places=2,  # Количество цифр после запятой.
        verbose_name="Цена",
        validators=[MinValueValidator(0)],  # Цена не может быть отрицательной.
    )
    socket = models.CharField(max_length=50, verbose_name="Сокет")  # Сокет процессора (строка, максимум 50 символов).
    image = models.ImageField(  # Изображение процессора.
        upload_to='cpu_images/', verbose_name="Изображение", blank=True, null=True # Изображения загружаются в директорию 'cpu_images/'. Поле может быть пустым.
    )
    integrated_graphics = models.BooleanField(  # Наличие интегрированной графики.
        default=False, verbose_name="Интегрированная графика" # По умолчанию - False.
    )

    def __str__(self):
        return f"{self.manufacturer} {self.model}"  # Возвращает строку, содержащую производителя и модель процессора.

    class Meta:
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"
        ordering = ['manufacturer', 'model']  # Сортировка по производителю, затем по модели.

    def is_compatible_with_motherboard(self, motherboard):
        """Проверяет совместимость сокета процессора и материнской платы."""
        return self.socket == motherboard.socket  # Проверяет, совпадают ли сокеты.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='cpu', component_id=self.id)  # Пытается получить информацию о запасах данного процессора.
            return stock.quantity > 0  # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist:  # Если информация о запасах не найдена.
            return False  # Возвращает False (товара нет в наличии).

    reviews = GenericRelation(
        'components.Review', related_query_name='cpu'
    )  # Use string representation to avoid circular import. Обобщенная связь с моделью Review (отзыв) для процессора.
    # related_query_name позволяет запрашивать отзывы, связанные с процессором, используя cpu__поле_отзыва.


# Определение модели Motherboard (Материнская плата)
class Motherboard(models.Model):
    """Материнская плата."""

    manufacturer = models.ForeignKey(  # Связь "один ко многим" с моделью Manufacturer.
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")  # Модель материнской платы.
    form_factor = models.CharField(max_length=50, verbose_name="Форм-фактор")  # Форм-фактор материнской платы (ATX, Micro-ATX и т.д.).
    socket = models.CharField(max_length=50, verbose_name="Сокет")  # Сокет процессора, поддерживаемый материнской платой.
    chipset = models.CharField(max_length=50, verbose_name="Чипсет")  # Чипсет материнской платы.
    ram_slots = models.IntegerField(verbose_name="Слоты для RAM")  # Количество слотов для оперативной памяти.
    ram_type = models.CharField(
        max_length=10, verbose_name="Тип RAM (DDR4, DDR5)"
    )  # Тип оперативной памяти, поддерживаемый материнской платой (DDR4, DDR5 и т.д.).
    max_ram_frequency = models.IntegerField(verbose_name="Максимальная частота RAM")  # Максимальная частота оперативной памяти, поддерживаемая.
    expansion_slots = models.TextField(verbose_name="Слоты расширения")  # Слоты расширения (PCIe, PCI и т.д.).
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )  # Цена материнской платы.
    image = models.ImageField(
        upload_to='motherboard_images/',
        verbose_name="Изображение",
        blank=True,
        null=True,
    )  # Изображение материнской платы.
    wifi = models.BooleanField(
        default=False, verbose_name="Wi-Fi"
    )  # Added WiFi support # Наличие Wi-Fi модуля на материнской плате.

    def __str__(self):
        return f"{self.manufacturer} {self.model}"  # Возвращает строку, содержащую производителя и модель материнской платы.

    class Meta:
        verbose_name = "Материнская плата"
        verbose_name_plural = "Материнские платы"
        ordering = ['manufacturer', 'model']  # Сортировка по производителю, затем по модели.

    def is_compatible_with_cpu(self, cpu):
        """Проверяет совместимость сокета материнской платы и процессора."""
        return self.socket == cpu.socket  # Проверяет, совпадают ли сокеты.

    def is_compatible_with_ram(self, ram):
        """Проверяет совместимость типа RAM и частоты."""
        return (
            self.ram_type == ram.type and self.max_ram_frequency >= ram.frequency
        )  # Проверяет совместимость типа и частоты оперативной памяти.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(
                component_type='motherboard', component_id=self.id
            )  # Пытается получить информацию о запасах данной материнской платы.
            return stock.quantity > 0  # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist:  # Если информация о запасах не найдена.
            return False  # Возвращает False (товара нет в наличии).

    reviews = GenericRelation(
        'components.Review', related_query_name='motherboard'
    ) # Обобщенная связь с моделью Review (отзыв) для материнской платы.


# Определение модели RAM (Оперативная память)
class RAM(models.Model):
    """Оперативная память."""

    manufacturer = models.ForeignKey(  # Связь "один ко многим" с моделью Manufacturer.
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")  # Модель оперативной памяти.
    capacity = models.IntegerField(verbose_name="Объем (ГБ)")  # Объем оперативной памяти в ГБ.
    frequency = models.IntegerField(verbose_name="Частота (МГц)")  # Частота оперативной памяти в МГц.
    type = models.CharField(max_length=10, verbose_name="Тип (DDR4, DDR5)")  # Тип оперативной памяти (DDR4, DDR5 и т.д.).
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )  # Цена оперативной памяти.
    image = models.ImageField(
        upload_to='ram_images/', verbose_name="Изображение", blank=True, null=True
    )  # Изображение оперативной памяти.
    rgb = models.BooleanField(
        default=False, verbose_name="RGB подсветка"
    )  # Added RGB lighting # Наличие RGB подсветки.

    def __str__(self):
        return (
            f"{self.manufacturer} {self.model} ({self.capacity} ГБ, "
            f"{self.frequency} МГц)"
        )  # Возвращает строку, содержащую производителя, модель, объем и частоту оперативной памяти.

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"
        ordering = ['manufacturer', 'model']  # Сортировка по производителю, затем по модели.

    def is_compatible_with_motherboard(self, motherboard):
        """Проверяет совместимость типа RAM и частоты с материнской платой."""
        return (
            self.type == motherboard.ram_type
            and self.frequency <= motherboard.max_ram_frequency
        )  # Проверяет совместимость типа и частоты оперативной памяти с материнской платой.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='ram', component_id=self.id)  # Пытается получить информацию о запасах данной оперативной памяти.
            return stock.quantity > 0  # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist:  # Если информация о запасах не найдена.
            return False  # Возвращает False (товара нет в наличии).

    reviews = GenericRelation('components.Review', related_query_name='ram') # Обобщенная связь с моделью Review (отзыв) для оперативной памяти.


# Определение модели GPU (Видеокарта)
class GPU(models.Model):
    """Видеокарта."""

    manufacturer = models.ForeignKey(  # Связь "один ко многим" с моделью Manufacturer.
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")  # Модель видеокарты.
    memory = models.IntegerField(verbose_name="Объем памяти (ГБ)")  # Объем видеопамяти в ГБ.
    frequency = models.FloatField(verbose_name="Частота (ГГц)")  # Частота ядра видеокарты в ГГц.
    tdp = models.IntegerField(verbose_name="TDP (Вт)")  # TDP (Thermal Design Power) видеокарты в Вт.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )  # Цена видеокарты.
    image = models.ImageField(
        upload_to='gpu_images/', verbose_name="Изображение", blank=True, null=True
    )  # Изображение видеокарты.
    interface = models.CharField(
        max_length=50, verbose_name="Интерфейс", default="PCIe x16"
    )  # Добавлено поле interface # Интерфейс подключения видеокарты (PCIe x16 и т.д.).
    ray_tracing = models.BooleanField(
        default=False, verbose_name="Поддержка Ray Tracing"
    )  # Added Ray Tracing Support # Поддержка технологии Ray Tracing.

    def __str__(self):
        return f"{self.manufacturer} {self.model}"  # Возвращает строку, содержащую производителя и модель видеокарты.

    class Meta:
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"
        ordering = ['manufacturer', 'model']  # Сортировка по производителю, затем по модели.

    def is_power_compatible(self, psu):
        """Проверяет, достаточно ли мощности блока питания для видеокарты."""
        return self.tdp <= psu.power  # Проверяет, достаточно ли мощности блока питания для TDP видеокарты.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='gpu', component_id=self.id)  # Пытается получить информацию о запасах данной видеокарты.
            return stock.quantity > 0  # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist:  # Если информация о запасах не найдена.
            return False  # Возвращает False (товара нет в наличии).

    reviews = GenericRelation('components.Review', related_query_name='gpu') # Обобщенная связь с моделью Review (отзыв) для видеокарты.


# Определение модели Storage (Накопитель)
class Storage(models.Model):
    """Накопитель (SSD/HDD)."""

    manufacturer = models.ForeignKey(  # Связь "один ко многим" с моделью Manufacturer.
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")  # Модель накопителя.
    capacity = models.IntegerField(verbose_name="Объем (ГБ/ТБ)")  # Объем накопителя в ГБ или ТБ.
    type = models.CharField(max_length=10, verbose_name="Тип (SSD/HDD)")  # Тип накопителя (SSD или HDD).
    interface = models.CharField(max_length=50, verbose_name="Интерфейс")  # Интерфейс подключения накопителя (SATA, NVMe и т.д.).
    read_speed = models.IntegerField(verbose_name="Скорость чтения (МБ/с)")  # Скорость чтения в МБ/с.
    write_speed = models.IntegerField(verbose_name="Скорость записи (МБ/с)")  # Скорость записи в МБ/с.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )  # Цена накопителя.
    image = models.ImageField(
        upload_to='storage_images/',
        verbose_name="Изображение",
        blank=True,
        null=True,
    )  # Изображение накопителя.
    nvme = models.BooleanField(
        default=False, verbose_name="NVMe Support"
    )  # Added NVMe Support # Поддержка NVMe.

    def __str__(self):
        return (
            f"{self.manufacturer} {self.model} ({self.capacity} ГБ, "
            f"{self.type})"
        )  # Возвращает строку, содержащую производителя, модель, объем и тип накопителя.

    class Meta:
        verbose_name = "Накопитель"
        verbose_name_plural = "Накопители"
        ordering = ['manufacturer', 'model']  # Сортировка по производителю, затем по модели.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='storage', component_id=self.id)  # Пытается получить информацию о запасах данного накопителя.
            return stock.quantity > 0  # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist:  # Если информация о запасах не найдена.
            return False  # Возвращает False (товара нет в наличии).

    reviews = GenericRelation('components.Review', related_query_name='storage') # Обобщенная связь с моделью Review (отзыв) для накопителя.


# Определение модели PSU (Блок питания)
class PSU(models.Model):
    """Блок питания."""

    manufacturer = models.ForeignKey(  # Связь "один ко многим" с моделью Manufacturer.
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    )
    model = models.CharField(max_length=255, verbose_name="Модель")  # Модель блока питания.
    power = models.IntegerField(verbose_name="Мощность (Вт)")  # Мощность блока питания в Вт.
    certification = models.CharField(max_length=50, verbose_name="Сертификация")  # Сертификация блока питания (80 Plus и т.д.).
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    )  # Цена блока питания.
    image = models.ImageField(
        upload_to='psu_images/', verbose_name="Изображение", blank=True, null=True
    )  # Изображение блока питания.
    modular = models.BooleanField(
        default=False, verbose_name="Модульный"
    )  # Added Modular Support # Модульность блока питания.

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.power} Вт)"  # Возвращает строку, содержащую производителя, модель и мощность блока питания.

    class Meta:
        verbose_name = "Блок питания"
        verbose_name_plural = "Блоки питания"
        ordering = ['manufacturer', 'model']  # Сортировка по производителю, затем по модели.
        unique_together = ['manufacturer', 'model']  # Ensure manufacturer + model is unique # Гарантирует уникальность комбинации производителя и модели.

    def is_sufficient_for_gpu(self, gpu):
        """Проверяет, достаточно ли мощности блока питания для видеокарты."""
        return self.power >= gpu.tdp  # Проверяет, достаточно ли мощности блока питания для TDP видеокарты.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='psu', component_id=self.id)  # Пытается получить информацию о запасах данного блока питания.
            return stock.quantity > 0  # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist:  # Если информация о запасах не найдена.
            return False  # Возвращает False (товара нет в наличии).

    reviews = GenericRelation('components.Review', related_query_name='psu') # Обобщенная связь с моделью Review (отзыв) для блока питания.


class Case(models.Model):
    """Корпус."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    ) # Связь "один ко многим" с моделью Manufacturer. При удалении производителя, удаляются все связанные корпуса.
    model = models.CharField(max_length=255, verbose_name="Модель") # Модель корпуса.
    form_factor = models.CharField(max_length=50, verbose_name="Форм-фактор") # Форм-фактор корпуса (ATX, Micro-ATX и т.д.).
    dimensions = models.CharField(max_length=50, verbose_name="Размеры") # Размеры корпуса.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    ) # Цена корпуса. Валидатор гарантирует, что цена не отрицательная.
    image = models.ImageField(
        upload_to='case_images/', verbose_name="Изображение", blank=True, null=True
    ) # Изображение корпуса. Загружается в папку 'case_images'.  Поле может быть пустым.
    supported_motherboard_form_factors = models.CharField(
        max_length=255,
        verbose_name="Поддерживаемые форм-факторы мат. плат",
        default="ATX, Micro-ATX, Mini-ITX",
    ) # Поддерживаемые форм-факторы материнских плат. Значение по умолчанию: "ATX, Micro-ATX, Mini-ITX".
    side_panel_window = models.BooleanField(
        default=False, verbose_name="Боковое окно"
    )  # Added Side Panel Window # Наличие бокового окна в корпусе.

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.form_factor})" # Возвращает строку, содержащую производителя, модель и форм-фактор корпуса.

    class Meta:
        verbose_name = "Корпус"
        verbose_name_plural = "Корпуса"
        ordering = ['manufacturer', 'model'] # Сортировка по производителю, затем по модели.

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='case', component_id=self.id) # Пытается получить информацию о запасах данного корпуса.
            return stock.quantity > 0 # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist: # Если информация о запасах не найдена.
            return False # Возвращает False (товара нет в наличии).

    reviews = GenericRelation('components.Review', related_query_name='case') # Обобщенная связь с моделью Review (отзыв) для корпуса.


class Build(models.Model):
    """Сборка компьютера."""

    name = models.CharField(
        max_length=255,
        verbose_name="Название сборки",
        blank=True,
        null=True,
    )  # Добавил поле название сборки # Название сборки. Может быть пустым.
    cpu = models.ForeignKey(
        CPU,
        on_delete=models.CASCADE,
        verbose_name="Процессор",
        related_name='builds',
    ) # Связь "один ко многим" с моделью CPU (процессор). При удалении процессора, удаляется и сборка.
    # related_name='builds' позволяет получить все сборки, в которых используется данный процессор, через cpu.builds.all()
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.CASCADE,
        verbose_name="Материнская плата",
        blank=True,
        null=True,
        related_name='builds',
    ) # Связь "один ко многим" с моделью Motherboard (материнская плата). Может быть пустым.
    ram = models.ForeignKey(
        RAM,
        on_delete=models.CASCADE,
        verbose_name="Оперативная память",
        blank=True,
        null=True,
        related_name='builds',
    ) # Связь "один ко многим" с моделью RAM (оперативная память). Может быть пустым.
    gpu = models.ForeignKey(
        GPU,
        on_delete=models.CASCADE,
        verbose_name="Видеокарта",
        blank=True,
        null=True,
        related_name='builds',
    ) # Связь "один ко многим" с моделью GPU (видеокарта). Может быть пустым.
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name="Накопитель",
        blank=True,
        null=True,
        related_name='builds',
    ) # Связь "один ко многим" с моделью Storage (накопитель). Может быть пустым.
    psu = models.ForeignKey(
        PSU,
        on_delete=models.CASCADE,
        verbose_name="Блок питания",
        blank=True,
        null=True,
        related_name='builds',
    ) # Связь "один ко многим" с моделью PSU (блок питания). Может быть пустым.
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        verbose_name="Корпус",
        blank=True,
        null=True,
        related_name='builds',
    ) # Связь "один ко многим" с моделью Case (корпус). Может быть пустым.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='builds',
        blank=True,
        null=True,
    ) # Связь "один ко многим" с моделью User (пользователь). Может быть пустым.

    def __str__(self):
        return (
            f"Сборка {self.pk} - {self.name if self.name else 'Без имени'}"
        ) # Возвращает строку, содержащую ID сборки и ее название (если есть).

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
        return price # Возвращает общую стоимость сборки.

    class Meta:
        verbose_name = "Сборка"
        verbose_name_plural = "Сборки"
        ordering = ['name'] # Сортировка по названию сборки.


class Cooler(models.Model):
    """Охлаждение (кулер для CPU)."""

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель"
    ) # Связь "один ко многим" с моделью Manufacturer.
    model = models.CharField(max_length=255, verbose_name="Модель") # Модель кулера.
    cooler_type = models.CharField(
        max_length=50,
        verbose_name="Тип охлаждения",
        choices=[
            ('air', 'Воздушное'),
            ('liquid', 'Жидкостное'),
        ],
    ) # Тип охлаждения (воздушное или жидкостное).
    fan_size = models.IntegerField(
        verbose_name="Размер вентилятора (мм)", blank=True, null=True
    )  # Только для воздушных # Размер вентилятора в мм. Только для воздушных кулеров. Может быть пустым.
    radiator_size = models.CharField(
        max_length=50,
        verbose_name="Размер радиатора",
        blank=True,
        null=True,
    )  # Только для жидкостных # Размер радиатора. Только для жидкостных кулеров. Может быть пустым.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)],
    ) # Цена кулера.
    image = models.ImageField(
        upload_to='cooler_images/', verbose_name="Изображение", blank=True, null=True
    ) # Изображение кулера.
    rgb = models.BooleanField(
        default=False, verbose_name="RGB подсветка"
    )  # Added RGB lighting # Наличие RGB подсветки.

    def __str__(self):
        return f"{self.manufacturer} {self.model}" # Возвращает строку, содержащую производителя и модель кулера.

    class Meta:
        verbose_name = "Охлаждение"
        verbose_name_plural = "Охлаждения"
        ordering = ['manufacturer', 'model'] # Сортировка по производителю, затем по модели.

    def is_compatible_with_cpu(self, cpu):
        """Проверяет совместимость с CPU."""
        # Добавьте логику проверки (например, сокет, TDP и т.д.)
        return True  # Заглушка # TODO: Implement real compatibility check

    def has_stock(self):
        """Проверяет, есть ли товар в наличии."""
        try:
            stock = Stock.objects.get(component_type='cooler', component_id=self.id) # Пытается получить информацию о запасах данного кулера.
            return stock.quantity > 0 # Возвращает True, если количество на складе больше 0.
        except Stock.DoesNotExist: # Если информация о запасах не найдена.
            return False # Возвращает False (товара нет в наличии).

    reviews = GenericRelation('components.Review', related_query_name='cooler') # Обобщенная связь с моделью Review (отзыв) для кулера.


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
    ) # Тип компонента, для которого ведется учет запасов. Выбор из предопределенного списка.
    component_id = models.PositiveIntegerField(verbose_name="ID компонента") # ID компонента в соответствующей таблице.
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество") # Количество компонентов на складе.

    def __str__(self):
        return f"{self.get_component_name()} - {self.quantity}" # Возвращает строку, содержащую название компонента и его количество на складе.

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
        }.get(self.component_type) # Получает модель компонента по его типу.

        if component_model:
            try:
                component = component_model.objects.get(pk=self.component_id) # Пытается получить экземпляр компонента по ID.
                return f"{component.manufacturer} {component.model}" # Возвращает название компонента (производитель + модель).
            except component_model.DoesNotExist:
                return "Компонент не найден" # Возвращает сообщение, если компонент не найден.
        else:
            return "Неизвестный тип компонента" # Возвращает сообщение, если тип компонента неизвестен.

    def get_component_type_display(self):
        return dict(self.COMPONENT_TYPE_CHOICES).get(
            self.component_type, 'Unknown'
        ) # Возвращает удобочитаемое название типа компонента.

    class Meta:
        verbose_name = "Складской запас"
        verbose_name_plural = "Складские запасы"
        unique_together = (
            'component_type',
            'component_id',
        )  # Гарантирует уникальность записи для каждого компонен # Гарантирует, что для каждого типа и ID компонента будет только одна запись в таблице запасов.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь") # Связь "один ко многим" с моделью User (пользователь).
    text = models.TextField(verbose_name="Текст отзыва") # Текст отзыва.
    rating = models.IntegerField(choices=[(1, "1 звезда"), (2, "2 звезды"), (3, "3 звезды"), (4, "4 звезды"),
                                           (5, "5 звезд")], verbose_name="Рейтинг") # Рейтинг от 1 до 5 звезд.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания") # Дата создания отзыва. Автоматически устанавливается при создании.
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления") # Дата обновления отзыва. Автоматически обновляется при каждом изменении.

    # Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Тип контента, к которому относится отзыв (CPU, GPU и т.д.).
    object_id = models.PositiveIntegerField() # ID объекта, к которому относится отзыв.
    content_object = GenericForeignKey('content_type', 'object_id') # Обобщенный внешний ключ, связывающий отзыв с конкретным объектом (например, CPU).

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at'] # Сортировка по дате создания (от новых к старым).

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.content_object}" # Возвращает строку, содержащую имя пользователя и объект, на который оставлен отзыв.