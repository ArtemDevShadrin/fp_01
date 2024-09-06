from django.db import models
from apps.orders.models import Order


class Report(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="ID заказа",
    )
    report_date = models.DateField(auto_now_add=True, verbose_name="Дата отчета")
    sales_data = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Данные по продажам"
    )
    profit = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Прибыль"
    )
    expenses = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Расходы"
    )

    def __str__(self):
        return f"Отчет {self.id} - Заказ {self.order.id}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ["-report_date"]
