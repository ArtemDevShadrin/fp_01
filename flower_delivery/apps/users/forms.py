from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Пароль должен содержать не менее 8 символов.")
    if not re.findall(r"\d", value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
    if not re.findall('[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(
            "Пароль должен содержать хотя бы один специальный символ."
        )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Введите ваш действующий email.")
    phone_number = PhoneNumberField(
        region="RU",
        required=True,
        help_text="Введите номер телефона в международном формате.",
    )
    address = forms.CharField(
        widget=forms.Textarea, required=False, help_text="Введите ваш полный адрес."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Пароль должен содержать не менее 8 символов, включать цифры и специальные символы.",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль еще раз для подтверждения.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "address"]


class UserProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Введите ваш действующий email.")
    phone_number = PhoneNumberField(
        region="RU",
        required=False,
        help_text="Введите номер телефона в международном формате.",
    )
    address = forms.CharField(
        widget=forms.Textarea, required=False, help_text="Введите ваш полный адрес."
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "address"]


class Meta:
    model = User
    fields = ["username", "email", "phone_number", "address", "password1", "password2"]
    error_messages = {
        "username": {
            "required": "Введите имя пользователя.",
            "invalid": "Введите корректное имя пользователя.",
        },
        "email": {
            "required": "Введите адрес электронной почты.",
            "invalid": "Введите корректный адрес электронной почты.",
        },
        "phone_number": {
            "required": "Введите номер телефона.",
            "invalid": "Введите корректный номер телефона.",
        },
        "address": {
            "required": "Введите ваш адрес.",
        },
        "password1": {
            "required": "Введите пароль.",
        },
        "password2": {
            "required": "Введите подтверждение пароля.",
            "password_mismatch": "Пароли не совпадают.",
        },
    }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User  # Обязательно указываем модель
        fields = ["username", "email", "phone_number", "address"]
