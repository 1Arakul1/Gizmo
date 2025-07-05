# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Электронная почта",
        required=True,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')  # Убираем 'password'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password2")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TopUpBalanceForm(forms.Form):
    amount = forms.DecimalField(
        label="Сумма пополнения",
        min_value=0.01,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Электронная почта",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    card_number = forms.CharField(
        label="Номер карты",
        max_length=16,  # Стандартная длина номера карты
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    card_expiry = forms.CharField(
        label="Срок действия карты (ММ/ГГ)",
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    card_cvv = forms.CharField(
        label="CVV",
        max_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit():
            raise forms.ValidationError("Номер карты должен содержать только цифры.")
        if len(card_number) != 16: #Имитация проверки длины
            raise forms.ValidationError("Номер карты должен состоять из 16 цифр.")
        return card_number

    def clean_card_expiry(self):
        card_expiry = self.cleaned_data['card_expiry']
        # Здесь можно добавить более сложную валидацию формата и срока действия
        return card_expiry

    def clean_card_cvv(self):
        card_cvv = self.cleaned_data['card_cvv']
        if not card_cvv.isdigit():
            raise forms.ValidationError("CVV должен содержать только цифры.")
        if len(card_cvv) != 3: #Имитация проверки длины
            raise forms.ValidationError("CVV должен состоять из 3 цифр.")
        return card_cvv


class ConfirmTopUpForm(forms.Form):
    confirmation_code = forms.CharField(
        label="Код подтверждения",
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_confirmation_code(self):
        confirmation_code = self.cleaned_data['confirmation_code']
        if not confirmation_code.isdigit():
            raise forms.ValidationError("Код подтверждения должен содержать только цифры.")
        if len(confirmation_code) != 6:
             raise forms.ValidationError("Код подтверждения должен состоять из 6 цифр.")
        return confirmation_code