from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.reviews.models import Review
from apps.catalog.models import Product
from apps.reviews.forms import ReviewForm

User = get_user_model()


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product", price=50.00, quantity=10
        )
        self.review = Review.objects.create(
            product=self.product, user=self.user, rating=5, comment="Отличный продукт!"
        )

    def test_review_creation(self):
        self.assertIsInstance(self.review, Review)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Отличный продукт!")

    def test_review_deletion(self):
        self.review.delete()
        self.assertEqual(Review.objects.count(), 0)


class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product", price=50.00, quantity=10
        )

    def test_valid_review_form(self):
        form_data = {"rating": 4, "comment": "Хороший продукт!"}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_review_form(self):
        form_data = {"rating": 10, "comment": ""}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product", price=50.00, quantity=10
        )
        self.client.login(username="testuser", password="12345")

    def test_add_review_view(self):
        form_data = {"rating": 5, "comment": "Отличный продукт!"}
        response = self.client.post(
            reverse("add_review", args=[self.product.id]), data=form_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after review creation

    def test_product_reviews_view(self):
        response = self.client.get(reverse("product_reviews", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/product_reviews.html")


class ReviewURLsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product", price=50.00, quantity=10
        )

    def test_add_review_url(self):
        url = reverse("add_review", args=[self.product.id])
        self.assertEqual(url, f"/reviews/product/{self.product.id}/add_review/")

    def test_product_reviews_url(self):
        url = reverse("product_reviews", args=[self.product.id])
        self.assertEqual(url, f"/reviews/product/{self.product.id}/reviews/")


class ReviewTemplateRenderingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product", price=50.00, quantity=10
        )

    def test_product_reviews_template(self):
        response = self.client.get(reverse("product_reviews", args=[self.product.id]))
        self.assertTemplateUsed(response, "reviews/product_reviews.html")

    def test_add_review_template(self):
        form_data = {"rating": 5, "comment": "Отличный продукт!"}
        response = self.client.post(
            reverse("add_review", args=[self.product.id]), data=form_data
        )
        self.assertEqual(response.status_code, 302)


class ContextProcessorTest(TestCase):
    def test_cart_item_count_processor(self):
        response = self.client.get(reverse("product_list"))
        self.assertIn("cart_item_count", response.context)
