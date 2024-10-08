# Generated by Django 5.1 on 2024-08-29 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_orderdetail"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="products_new",
        ),
        migrations.RemoveField(
            model_name="orderdetail",
            name="delivery_address",
        ),
        migrations.RemoveField(
            model_name="orderdetail",
            name="order_date",
        ),
        migrations.RemoveField(
            model_name="orderdetail",
            name="order_number",
        ),
        migrations.RemoveField(
            model_name="orderdetail",
            name="user",
        ),
        migrations.AddField(
            model_name="orderdetail",
            name="order",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="orders.order",
            ),
            preserve_default=False,
        ),
    ]
