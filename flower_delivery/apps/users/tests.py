from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.users.forms import UserRegistrationForm, UserLoginForm, UserProfileEditForm
from django.core.management import call_command

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="testuser@example.com",
            phone_number="+79999999999",
            address="Test Address",
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpass123"))

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")


class UserFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_valid_registration_form(self):
        form_data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "phone_number": "+79999999999",
            "address": "Test Address 2",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form(self):
        form_data = {
            "username": "",
            "email": "invalidemail",
            "phone_number": "invalidphone",
            "address": "",
            "password1": "pass",
            "password2": "pass",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_login_form(self):
        form_data = {"username": "testuser", "password": "testpass123"}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_profile_edit_form(self):
        form_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "phone_number": "+79999999999",
            "address": "Updated Address",
        }
        form = UserProfileEditForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_profile_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_edit_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_edit.html")


class UserURLsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_register_url(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)


class UserTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_register_template_used(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "users/register.html")

    def test_login_template_used(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "users/login.html")

    def test_profile_template_used(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertTemplateUsed(response, "users/profile.html")


class ContextProcessorTest(TestCase):
    def test_cart_item_count_processor(self):
        session = self.client.session
        session["cart"] = {"1": {"quantity": 2, "price": 10.99}}
        session.save()
        response = self.client.get(reverse("login"))
        self.assertEqual(response.context["cart_item_count"], 2)


class ManagementCommandsTest(TestCase):
    def test_custom_management_command(self):
        call_command("showmigrations", "--plan")
