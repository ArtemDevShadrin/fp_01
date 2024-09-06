import subprocess
import sys
from django.core.management.base import BaseCommand
import threading


class Command(BaseCommand):
    help = "Запуск Django сервера и Telegram бота"

    def handle(self, *args, **kwargs):
        def start_django_server():
            subprocess.run([sys.executable, "manage.py", "runserver"])

        def start_telegram_bot():
            subprocess.run([sys.executable, "manage.py", "startbot"])

        django_thread = threading.Thread(target=start_django_server)
        bot_thread = threading.Thread(target=start_telegram_bot)

        django_thread.start()
        bot_thread.start()

        django_thread.join()
        bot_thread.join()
