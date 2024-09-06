from django import forms
from .models import Report
from apps.catalog.models import Product
from apps.users.models import User


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["order", "sales_data", "profit", "expenses"]
        labels = {
            "order": "ID заказа",
            "sales_data": "Данные по продажам",
            "profit": "Прибыль",
            "expenses": "Расходы",
        }


class ReportFilterForm(forms.Form):
    date_start = forms.DateField(
        label="Дата начала",
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    date_end = forms.DateField(
        label="Дата окончания",
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    report_type = forms.ChoiceField(
        choices=[
            ("products", "По товарам"),
            ("customers", "По клиентам"),
            ("date", "По дате"),
            ("period", "За период"),
        ],
        required=True,
    )


class AnalyticsFilterForm(forms.Form):
    product_type = forms.ModelChoiceField(
        queryset=Product.objects.all(), required=False, label="Тип товара"
    )
    client = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False, label="Клиент"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата начала",
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата окончания",
    )
