from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product
from django.core.management import call_command

User = get_user_model()


class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.99,
            quantity=100,
        )

    def test_product_creation(self):
        """Проверка создания продукта"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 10.99)
        self.assertEqual(self.product.quantity, 100)

    def test_product_is_in_stock(self):
        """Проверка наличия продукта на складе"""
        self.assertTrue(self.product.is_in_stock())

    def test_product_str(self):
        """Проверка строкового представления продукта"""
        self.assertEqual(str(self.product), "Test Product")


class ProductViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.99,
            quantity=100,
        )
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_product_list_view(self):
        """Проверка страницы списка продуктов"""
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertTemplateUsed(response, "catalog/product_list.html")

    def test_product_detail_view(self):
        """Проверка страницы деталей продукта"""
        response = self.client.get(reverse("product_detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertTemplateUsed(response, "catalog/product_detail.html")


class ProductURLsTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.99,
            quantity=100,
        )

    def test_product_list_url(self):
        """Проверка URL страницы списка продуктов"""
        response = self.client.get("/product/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Проверка URL страницы деталей продукта"""
        response = self.client.get(f"/product/{self.product.pk}/")
        self.assertEqual(response.status_code, 200)


class ProductTemplateTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.99,
            quantity=100,
        )

    def test_product_list_template_used(self):
        """Проверка использования правильного шаблона на странице списка продуктов"""
        response = self.client.get(reverse("product_list"))
        self.assertTemplateUsed(response, "catalog/product_list.html")

    def test_product_detail_template_used(self):
        """Проверка использования правильного шаблона на странице деталей продукта"""
        response = self.client.get(reverse("product_detail", args=[self.product.pk]))
        self.assertTemplateUsed(response, "catalog/product_detail.html")


class ContextProcessorTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_cart_item_count_processor(self):
        """Проверка контекстного процессора для подсчета количества товаров в корзине"""
        session = self.client.session
        session["cart"] = {"1": {"quantity": 2, "price": 10.99}}
        session.save()

        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.context["cart_item_count"], 2)


class ManagementCommandsTest(TestCase):

    def test_custom_management_command(self):
        """Тестирование выполнения пользовательской команды"""
        # Для примера можно использовать существующую или создать свою команду
        call_command("showmigrations", "--plan")
        # Если команда возвращает что-то, можно использовать self.assertEqual для проверки
