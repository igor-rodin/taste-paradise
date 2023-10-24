from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={"placeholder": "Имя пользователя", "class": "control__input"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"placeholder": "user@mail.com", "class": "control__input"}
        ),
    )
    password1 = forms.CharField(
        label="Пароль",
        help_text="Не менее 8 символов",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Пароль", "class": "control__input"}
        ),
    )
    password2 = forms.CharField(
        label="Подтерждение пароля",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Потверждение пароля", "class": "control__input"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={"placeholder": "Имя пользователя", "class": "control__input"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        help_text="Не менее 8 символов",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Пароль", "class": "control__input"}
        ),
    )
