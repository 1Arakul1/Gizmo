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
        min_value=0.01,  # Минимальная сумма для пополнения
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

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