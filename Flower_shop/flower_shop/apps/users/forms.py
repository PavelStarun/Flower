from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        min_length=3,
        max_length=30,
        required=True,
        validators=[MinLengthValidator(3)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Введите логин',
            'style': 'width: 250px;',  # Установка ширины логина
        }),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Введите пароль',
            'style': 'width: 250px;',  # Установка ширины пароля
        }),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Повторите пароль',
            'style': 'width: 250px;',  # Установка ширины подтверждения пароля
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #e6f7ff;'}))
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #e6f7ff;'}))
    telegram_nickname = forms.CharField(max_length=50, required=False, label='Никнейм в Telegram', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #e6f7ff;'}))
    birth_date = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(1950, 2025), attrs={'class': 'form-control', 'style': 'background-color: #e6f7ff;'}))
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'background-color: #e6f7ff;'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'telegram_nickname', 'birth_date', 'email']

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return super().save(commit=commit)