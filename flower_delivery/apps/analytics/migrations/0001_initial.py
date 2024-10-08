# Generated by Django 5.1 on 2024-08-31 05:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("orders", "0006_orderdetail_order_number_orderdetail_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("report_date", models.DateField(auto_now_add=True)),
                ("sales_data", models.DecimalField(decimal_places=2, max_digits=10)),
                ("profit", models.DecimalField(decimal_places=2, max_digits=10)),
                ("expenses", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reports",
                        to="orders.order",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отчет",
                "verbose_name_plural": "Отчеты",
                "ordering": ["-report_date"],
            },
        ),
    ]
