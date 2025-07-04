# components/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    CPU,
    GPU,
    Motherboard,
    RAM,
    Storage,
    PSU,
    Case,
    Cooler,
    Manufacturer,
    Review,
)

class UniqueManufacturerMixin:
    """
    Миксин для форм, чтобы проверять уникальность производителя и модели.
    """

    def clean(self):
        cleaned_data = super().clean()
        manufacturer = cleaned_data.get('manufacturer')
        model = cleaned_data.get('model')

        if manufacturer and model:
            # Проверяем, существует ли уже компонент с таким производителем и моделью
            model_class = self._meta.model
            # Исключаем текущий экземпляр, если это редактирование
            if self.instance:  # Check if it's an update
                existing_component = model_class.objects.filter(
                    manufacturer=manufacturer, model=model
                ).exclude(pk=self.instance.pk)  # Exclude the current instance
            else:
                existing_component = model_class.objects.filter(
                    manufacturer=manufacturer, model=model
                )

            if existing_component.exists():
                raise ValidationError(
                    f"Компонент с таким производителем и моделью уже существует."
                )

        return cleaned_data


class CPUForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = CPU
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='cpu'
        )


class GPUForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = GPU
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='gpu'
        )


class MotherboardForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = Motherboard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='motherboard'
        )


class RAMForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = RAM
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='ram'
        )


class StorageForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='storage'
        )


class PSUForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = PSU
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='psu'
        )


class CaseForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='case'
        )


class CoolerForm(UniqueManufacturerMixin, forms.ModelForm):
    class Meta:
        model = Cooler
        fields = '__all__'
        # ... (Настройка виджетов, если нужно) ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='cooler'
        )  # Ограничение по производителю


# Forms for searching
class ComponentSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)


class CPUSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='cpu'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    socket = forms.CharField(label="Сокет", required=False)
    integrated_graphics = forms.BooleanField(
        label="Интегрированное графическое ядро", required=False
    )


class GPUSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='gpu'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    memory = forms.IntegerField(label="Объем памяти (ГБ)", required=False)
    interface = forms.CharField(label="Интерфейс", required=False)
    ray_tracing = forms.BooleanField(
        label="Поддержка Ray Tracing", required=False
    )


class MotherboardSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='motherboard'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    socket = forms.CharField(label="Сокет", required=False)
    form_factor = forms.CharField(label="Форм-фактор", required=False)
    wifi = forms.BooleanField(label="Wi-Fi", required=False)


class RAMSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='ram'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    type = forms.CharField(label="Тип (DDR4, DDR5)", required=False)
    capacity = forms.IntegerField(label="Объем (ГБ)", required=False)
    rgb = forms.BooleanField(label="RGB подсветка", required=False)


class StorageSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='storage'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    type = forms.CharField(label="Тип (SSD/HDD)", required=False)
    capacity = forms.IntegerField(label="Объем (ГБ/ТБ)", required=False)
    nvme = forms.BooleanField(label="NVMe Support", required=False)


class PSUSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='psu'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    power = forms.IntegerField(label="Мощность (Вт)", required=False)
    certification = forms.CharField(label="Сертификация", required=False)
    modular = forms.BooleanField(label="Модульный", required=False)


class CaseSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='case'),
        label="Производитель",
        required=False,
        empty_label="Все производители",
    )
    form_factor = forms.CharField(label="Форм-фактор", required=False)
    dimensions = forms.CharField(label="Размеры", required=False)
    side_panel_window = forms.BooleanField(label="Боковое окно", required=False)


# components/forms.py

class CoolerSearchForm(forms.Form):
    q = forms.CharField(label="Поиск", required=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(component_type='cooler'),
        label="Производитель",
        required=False,
        empty_label="Все производители"  # Add this line
    )
    cooler_type = forms.ChoiceField(
        label="Тип охлаждения",
        required=False,
        choices=Cooler.cooler_type.field.choices,
    )
    fan_size = forms.IntegerField(label="Размер вентилятора (мм)", required=False)
    rgb = forms.BooleanField(label="RGB подсветка", required=False)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }