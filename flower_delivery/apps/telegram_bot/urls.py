from django.urls import path
from .views import bot_info_view

app_name = "telegram_bot"

urlpatterns = [
    path("bot-info/", bot_info_view, name="bot_info"),
]
