from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.cart.models import Cart

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Тестовый продукт", price=10, quantity=100
        )
        self.cart = Cart.objects.create(
            user=self.user, items={"1": {"quantity": 2, "price": 10}}
        )

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, "testuser")
        self.assertEqual(self.cart.items["1"]["quantity"], 2)

    def test_cart_str_representation(self):
        self.assertEqual(str(self.cart), f"Корзина {self.user.username}")


class CartFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Тестовый продукт", price=10, quantity=100
        )

    def test_add_to_cart_form(self):
        response = self.client.post(
            reverse("add_to_cart", args=[self.product.pk]), data={"quantity": 1}
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart")
        self.assertIn(str(self.product.pk), cart)
        self.assertEqual(cart[str(self.product.pk)]["quantity"], 1)


class CartViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Тестовый продукт", price=10, quantity=100
        )
        self.cart = Cart.objects.create(
            user=self.user, items={str(self.product.pk): {"quantity": 1, "price": 10}}
        )

    def test_cart_view(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина")

    def test_add_to_cart(self):
        response = self.client.post(
            reverse("add_to_cart", args=[self.product.pk]), data={"quantity": 1}
        )
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get("cart")
        self.assertIn(str(self.product.pk), cart)

    def test_checkout_view(self):
        session = self.client.session
        session["cart"] = {
            str(self.product.pk): {"quantity": 1, "price": self.product.price}
        }
        session.save()

        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)


class CartUrlsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_cart_url(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_url(self):
        product = Product.objects.create(
            name="Тестовый продукт", price=10, quantity=100
        )
        response = self.client.post(
            reverse("add_to_cart", args=[product.pk]), data={"quantity": 1}
        )
        self.assertEqual(response.status_code, 302)


class CartTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Тестовый продукт", price=10, quantity=100
        )
        self.cart = Cart.objects.create(
            user=self.user, items={str(self.product.pk): {"quantity": 1, "price": 10}}
        )

    def test_cart_template_used(self):
        response = self.client.get(reverse("cart"))
        self.assertTemplateUsed(response, "cart/cart.html")

    def test_checkout_template_used(self):
        session = self.client.session
        session["cart"] = {
            str(self.product.pk): {"quantity": 1, "price": self.product.price}
        }
        session.save()

        response = self.client.get(reverse("checkout"))
        self.assertTemplateUsed(response, "cart/checkout.html")


class ContextProcessorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Тестовый продукт", price=10, quantity=100
        )
        self.cart = Cart.objects.create(
            user=self.user, items={str(self.product.pk): {"quantity": 1, "price": 10}}
        )

    def test_cart_item_count_processor(self):
        session = self.client.session
        session["cart"] = {
            str(self.product.pk): {"quantity": 1, "price": self.product.price}
        }
        session.save()

        response = self.client.get(reverse("cart"))
        self.assertEqual(response.context["cart_item_count"], 1)
