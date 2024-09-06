from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.telegram_bot.models import User
from apps.telegram_bot.forms import TelegramLinkForm
from unittest.mock import patch


@patch("apps.telegram_bot.bot.dp.start_polling")
def test_telegram_bot_polling(self, mock_polling):
    mock_polling.assert_not_called()


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", telegram_id=123456789
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.telegram_id, 123456789)

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")


class TelegramLinkFormTest(TestCase):
    def test_valid_form(self):
        form_data = {"phone_number": "+71234567890"}
        form = TelegramLinkForm(data=form_data)
        self.assertTrue(form.is_valid())


class TelegramBotViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="12345", telegram_id=123456789
        )
        self.client.login(username="testuser", password="12345")

    def test_bot_info_view(self):
        response = self.client.get(reverse("telegram_bot:bot_info"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "telegram_bot/bot_info.html")


class TelegramBotURLsTest(TestCase):
    def test_bot_info_url(self):
        response = self.client.get("/telegram/bot-info/")
        self.assertEqual(response.status_code, 200)


class TelegramBotTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_bot_info_template_used(self):
        response = self.client.get(reverse("telegram_bot:bot_info"))
        self.assertTemplateUsed(response, "telegram_bot/bot_info.html")
