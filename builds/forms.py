# builds/forms.py
from django import forms
from .models import Order

class CustomOrderUpdateForm(forms.ModelForm):
    status = forms.ChoiceField(label='Статус заказа')  #  Определяем поле, но choices пока не задаем

    class Meta:
        model = Order
        fields = ['status'] # Только статус

    def __init__(self, *args, **kwargs):
        status_choices = kwargs.pop('status_choices', [])  # Получаем status_choices из kwargs
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = status_choices  # Устанавливаем choices для поля status


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class AddToCartForm(forms.Form):
    """Форма для добавления товара в корзину."""
    component_type = forms.ChoiceField(
        choices=[
            ('cpu', 'Процессор'),
            ('gpu', 'Видеокарта'),
            ('motherboard', 'Материнская плата'),
            ('ram', 'Оперативная память'),
            ('storage', 'Накопитель'),
            ('psu', 'Блок питания'),
            ('case', 'Корпус'),
            ('cooler', 'Охлаждение'),  # Добавлено
            ('build', 'Сборка'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тип компонента"
    )
    component_id = forms.IntegerField(widget=forms.HiddenInput())  # ID компонента или сборки
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Количество")