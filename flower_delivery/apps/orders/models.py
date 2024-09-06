from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from aiogram import Bot
from django.conf import settings
from apps.catalog.models import Product
from apps.users.models import User
from phonenumber_field.modelfields import PhoneNumberField
import requests
import logging

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
TELEGRAM_API_URL = (
    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
)


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", _("В ожидании")),
        ("Shipped", _("Отправлен")),
        ("Delivered", _("Доставлен")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="order_products")
    delivery_address = models.TextField()
    phone_number = PhoneNumberField(default="+70000000000")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    class Meta:
        ordering = ["-id"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField()
    delivery_address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)


logger = logging.getLogger(__name__)


def send_telegram_message_sync(user_id, message):
    data = {
        "chat_id": user_id,
        "text": message,
    }
    response = requests.post(TELEGRAM_API_URL, data=data)
    return response


@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    if created:
        message = f"""Ваш заказ #{instance.id} создан. И имеет статус: {instance.get_status_display()}
Когда заказ будет готов и передан курьеру мы вам сообщим) Ваш магазин цветов"""
        send_telegram_message_sync(instance.user.telegram_id, message)
    elif instance.status == "Shipped":
        message = f"""Ваш заказ #{instance.id}. Был передан курьеру. И имеет статус: {instance.get_status_display()}. Ваш магазин цветов"""
        send_telegram_message_sync(instance.user.telegram_id, message)
    elif instance.status == "Delivered":
        message = f"""Ваш заказ #{instance.id}. Был доставлен обладателю этих прекрасных цветов))) И имеет статус: {instance.get_status_display()}. Ваш магазин цветов"""
        send_telegram_message_sync(instance.user.telegram_id, message)
