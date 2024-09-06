from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django import forms
from .models import Order, OrderDetail, User
from .forms import OrderForm
from apps.catalog.models import Product


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/create_order.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("order_detail", kwargs={"pk": self.object.pk})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Получаем все заказы пользователя в обратном порядке
        orders = (
            Order.objects.filter(user=self.request.user)
            .select_related("user")
            .order_by("-created_at")
        )

        # Вычисляем общую сумму для каждого заказа и добавляем в контекст
        for order in orders:
            order.total_amount = order.details.aggregate(total=Sum("total_price"))[
                "total"
            ]

        return orders


class RepeatOrderView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)

        cart = request.session.get("cart", {})
        cart.clear()

        all_items_available = True

        for detail in order.details.all():
            product_id = str(detail.product.id)
            product = get_object_or_404(Product, pk=product_id)

            if product.quantity < detail.quantity:
                messages.error(
                    request,
                    f"Товар '{product.name}' в количестве {detail.quantity} шт. недоступен. Осталось на складе: {product.quantity} шт.",
                )
                all_items_available = False
            else:
                cart[product_id] = {
                    "quantity": detail.quantity,
                    "price": float(product.price),
                }

        if all_items_available:
            request.session["cart"] = cart
            messages.success(request, "Товары из заказа добавлены в корзину.")
        else:
            messages.warning(
                request,
                "Некоторые товары не были добавлены в корзину из-за отсутствия на складе.",
            )

        return redirect("cart")


class OrderFilterForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False, label="Пользователь"
    )
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES, required=False, label="Статус"
    )
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False, label="Дата с"
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False, label="Дата по"
    )


class OrderManagementView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_management.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = OrderFilterForm(self.request.GET)

        if form.is_valid():
            user = form.cleaned_data.get("user")
            status = form.cleaned_data.get("status")
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")

            if user:
                queryset = queryset.filter(user=user)
            if status:
                queryset = queryset.filter(status=status)
            if date_from:
                queryset = queryset.filter(created_at__date__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = OrderFilterForm(self.request.GET)
        return context

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class OrderStatusUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Order
    fields = ["status"]
    template_name = "orders/update_order_status.html"
    success_url = reverse_lazy("order_management")

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"


def change_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Pending", "Shipped", "Delivered"]:
            order.status = new_status
            order.save()
    return redirect("order_management")
