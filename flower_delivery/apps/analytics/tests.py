from django.test import TestCase, Client
from django.urls import reverse
from apps.analytics.models import Report
from django.db.models.signals import post_save
from apps.orders.models import Order, notify_order_status_change
from apps.analytics.forms import ReportForm, AnalyticsFilterForm
from apps.users.models import User


class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
            user=self.user, delivery_address="Test Address", phone_number="+70000000000"
        )
        post_save.disconnect(receiver=notify_order_status_change, sender=Order)

    def tearDown(self):
        post_save.connect(receiver=notify_order_status_change, sender=Order)

    def test_report_creation(self):
        report = Report.objects.create(
            order=self.order, sales_data=100.50, profit=50.00, expenses=30.00
        )
        self.assertEqual(report.sales_data, 100.50)

    def test_report_deletion(self):
        report = Report.objects.create(
            order=self.order, sales_data=100.50, profit=50.00, expenses=30.00
        )
        report.delete()
        self.assertEqual(Report.objects.count(), 0)


class ReportFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
            user=self.user, delivery_address="Test Address", phone_number="+70000000000"
        )

    def test_valid_report_form(self):
        form_data = {
            "order": self.order.id,
            "sales_data": 100.50,
            "profit": 50.00,
            "expenses": 30.00,
        }
        form = ReportForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_report_form(self):
        form_data = {
            "order": "",
            "sales_data": "invalid",
            "profit": -10.00,
            "expenses": "",
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())


class AnalyticsFilterFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_valid_filter_form(self):
        form_data = {
            "product_type": None,
            "client": self.user.id,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())


class AnalyticsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_report_list_view(self):
        response = self.client.get(reverse("report_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "analytics/report_list.html")

    def test_report_create_view(self):
        response = self.client.get(reverse("report_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "analytics/report_form.html")


class AnalyticsURLTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(
            user=self.user, delivery_address="Test Address", phone_number="+70000000000"
        )

    def test_report_list_url(self):
        url = reverse("report_list")
        self.assertEqual(url, "/analytics/reports/")

    def test_report_detail_url(self):
        report = Report.objects.create(
            order=self.order, sales_data=100, profit=50, expenses=30
        )
        url = reverse("report_detail", args=[report.id])
        self.assertEqual(url, f"/analytics/reports/{report.id}/")


class TemplateRenderingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()
        self.client.login(username="testuser", password="12345")

    def test_report_list_template(self):
        response = self.client.get(reverse("report_list"))
        self.assertTemplateUsed(response, "analytics/report_list.html")

    def test_report_create_template(self):
        response = self.client.get(reverse("report_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "analytics/report_list.html")


class ContextProcessorTest(TestCase):
    def test_cart_item_count_processor(self):
        response = self.client.get(reverse("cart"))
        self.assertIn("cart_item_count", response.context)
