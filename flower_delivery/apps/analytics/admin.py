from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "report_date", "order", "sales_data", "profit", "expenses")
    list_filter = ("report_date",)
    search_fields = ("order__id", "sales_data", "profit", "expenses")
