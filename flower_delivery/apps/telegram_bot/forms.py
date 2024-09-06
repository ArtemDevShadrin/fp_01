from django import forms


class TelegramLinkForm(forms.Form):
    phone_number = forms.CharField(
        label="Ваш номер телефона",
        max_length=15,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите номер телефона с кодом страны"}
        ),
    )
