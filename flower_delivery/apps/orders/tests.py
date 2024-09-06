from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Order

User = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
            user=self.user, delivery_address="Test Address", phone_number="+70000000000"
        )

    def test_order_creation(self):
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.delivery_address, "Test Address")


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
            user=self.user, delivery_address="Test Address", phone_number="+70000000000"
        )

    def test_order_list_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)


class OrderURLsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
            user=self.user, delivery_address="Test Address", phone_number="+70000000000"
        )

    def test_order_list_url(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
