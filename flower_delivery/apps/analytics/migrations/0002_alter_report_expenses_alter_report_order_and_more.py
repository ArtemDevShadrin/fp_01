# Generated by Django 5.1 on 2024-09-04 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0001_initial"),
        ("orders", "0007_alter_order_options_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="expenses",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Расходы"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reports",
                to="orders.order",
                verbose_name="ID заказа",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="profit",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Прибыль"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="report_date",
            field=models.DateField(auto_now_add=True, verbose_name="Дата отчета"),
        ),
        migrations.AlterField(
            model_name="report",
            name="sales_data",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Данные по продажам"
            ),
        ),
    ]
