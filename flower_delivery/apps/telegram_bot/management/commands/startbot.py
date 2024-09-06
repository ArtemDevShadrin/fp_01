from django.core.management.base import BaseCommand
from apps.telegram_bot.bot import main
import asyncio


class Command(BaseCommand):
    help = "Запуск телеграм-бота"

    def handle(self, *args, **kwargs):
        asyncio.run(main())
