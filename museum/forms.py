from django.contrib.auth.models import User
from django import forms
from .models import Order


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Логин', required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    email = forms.EmailField(widget=forms.EmailInput, label='Почта', required=True)
    username = forms.CharField(label='Логин', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password',]


class CreateOrderForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Имя')
    patronymic = forms.CharField(required=False, label='Отчество')
    last_name = forms.CharField(required=True, label='Фамилия')
    phone_num = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=True)
    email = forms.EmailField(widget=forms.EmailInput, label='Почта', required=True)
    country = forms.CharField(required=True, label='Страна')
    region = forms.CharField(required=True, label='Регион')
    city = forms.CharField(required=True, label='Город')
    street = forms.CharField(required=True, label='Улица')
    house = forms.CharField(required=True, label='Дом')
    flat = forms.CharField(required=True, label='Квартира')
    index = forms.CharField(required=True, label='Индекс')

    class Meta:
        model = Order
        fields = ['first_name', 'patronymic', 'last_name', 'phone_num', 'email', 'country', 'region', 'city', 'street',
                  'house', 'flat', 'index']