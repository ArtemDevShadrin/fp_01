from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Поля, которые будут отображаться в списке товаров
    search_fields = ('name',)  # Поиск по названию товара
