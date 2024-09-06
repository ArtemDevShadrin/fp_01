from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_address", "phone_number"]
        widgets = {
            "delivery_address": forms.Textarea(attrs={"rows": 3}),
            "phone_number": forms.TextInput(attrs={"type": "tel"}),
        }
