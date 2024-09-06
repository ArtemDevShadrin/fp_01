from django.shortcuts import render
from django.conf import settings
from aiogram import Bot

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


def bot_info_view(request):
    return render(request, "telegram_bot/bot_info.html")
