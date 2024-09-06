from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "delivery_address")
    list_filter = ("status", "user")
    search_fields = ("delivery_address",)
    list_editable = ("status",)

    def get_status_display(self, obj):
        return obj.get_status_display()

    get_status_display.short_description = "Статус"
