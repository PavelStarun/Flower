from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.forms import ModelForm



class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин',
            'class': 'form-control',
            'autocomplete': 'off',
            'value': ''
        }),
        validators=[MinLengthValidator(3, "Логин должен содержать не менее 3 символов.")]
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль',
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин',
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-control',
            'autocomplete': 'off'
        })
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