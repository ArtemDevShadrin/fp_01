from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django import forms
from django.views import View
from django.db.models import Sum
from .models import Report
from .forms import ReportForm, AnalyticsFilterForm
from apps.orders.models import Order, OrderDetail, Product, User


class ReportFilterForm(forms.Form):
    report_type = forms.ChoiceField(
        choices=[
            ("products", "По товарам"),
            ("clients", "По клиентам"),
            ("dates", "По датам"),
            ("period", "По периоду"),
        ]
    )
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget)
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(
                "Дата начала должна быть раньше даты окончания."
            )
        return cleaned_data


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "analytics/report_list.html"
    context_object_name = "reports"
    form_class = ReportFilterForm

    def get_queryset(self):
        queryset = super().get_queryset()

        report_type = self.request.GET.get("report_type")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if report_type:
            if report_type == "products":
                queryset = queryset.order_by("order__product__name")
            elif report_type == "clients":
                queryset = queryset.order_by("order__user__username")
            elif report_type == "dates":
                queryset = queryset.order_by("report_date")
            elif report_type == "period":
                if start_date and end_date:
                    queryset = queryset.filter(
                        report_date__range=[start_date, end_date]
                    )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.GET or None)
        return context


class ReportDetailView(DetailView):
    model = Report
    template_name = "analytics/report_detail.html"
    context_object_name = "report"


class ReportManagementView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Report
    template_name = "analytics/report_management.html"
    context_object_name = "reports"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class AnalyticsOverviewView(View):
    def get(self, request):
        reports = Report.objects.all()
        return render(
            request, "analytics/analytics_overview.html", {"reports": reports}
        )


class ReportCreateView(View):
    def get(self, request):
        form = ReportForm()
        return render(request, "analytics/report_form.html", {"form": form})

    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("report_list")
        return render(request, "analytics/report_form.html", {"form": form})


class AnalyticsView(View):
    def get(self, request):
        form = AnalyticsFilterForm()
        results = None
        total_sum = 0
        if "filter" in request.GET:
            form = AnalyticsFilterForm(request.GET)
            if form.is_valid():
                product_type = form.cleaned_data["product_type"]
                client = form.cleaned_data["client"]
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]

                results = OrderDetail.objects.all()

                if product_type:
                    results = results.filter(product=product_type)

                if client:
                    results = results.filter(order__user=client)

                if start_date:
                    results = results.filter(order_date__gte=start_date)

                if end_date:
                    results = results.filter(order_date__lte=end_date)

                results = (
                    results.values("product__name", "order__user__username")
                    .annotate(
                        total_quantity=Sum("quantity"), total_price=Sum("total_price")
                    )
                    .order_by("product__name")
                )

                # Вычисление общей суммы
                total_sum = sum(result["total_price"] for result in results)

        return render(
            request,
            "analytics/analytics.html",
            {"form": form, "results": results, "total_sum": total_sum},
        )
