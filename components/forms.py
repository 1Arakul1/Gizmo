# components/forms.py
from django import forms

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


class CPUForm(forms.ModelForm):
    class Meta:
        model = CPU
        fields = '__all__'  # или перечислите поля явно: ['manufacturer', 'model', 'cores', 'frequency', 'tdp', 'price', 'socket', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='cpu'
        )


class GPUForm(forms.ModelForm):
    class Meta:
        model = GPU
        fields = '__all__'  # или перечислите поля явно

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='gpu'
        )


class MotherboardForm(forms.ModelForm):
    class Meta:
        model = Motherboard
        fields = '__all__'  # или перечислите поля явно

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='motherboard'
        )


class RAMForm(forms.ModelForm):
    class Meta:
        model = RAM
        fields = '__all__'  # или перечислите поля явно

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='ram'
        )


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'  # или перечислите поля явно

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='storage'
        )


class PSUForm(forms.ModelForm):
    class Meta:
        model = PSU
        fields = '__all__'  # или перечислите поля явно

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='psu'
        )


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'  # или перечислите поля явно

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='case'
        )


class CoolerForm(forms.ModelForm):
    class Meta:
        model = Cooler
        fields = '__all__'  # или укажите поля
        # ... (Настройка виджетов, если нужно) ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].queryset = Manufacturer.objects.filter(
            component_type='cooler'
        )  # Ограничение по производителю


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
