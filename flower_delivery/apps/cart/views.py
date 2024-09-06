from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.utils import timezone
from apps.catalog.models import Product
from apps.orders.forms import OrderForm
from ..orders.models import Order, OrderDetail


def check_product_availability(product, requested_quantity):
    return requested_quantity <= product.quantity


class AddToCartView(View):

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(
                request, "Вы должны войти в систему, чтобы добавить товар в корзину."
            )
            return HttpResponseRedirect(reverse("login") + f"?next={request.path}")

        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get("quantity", 1))

        if not check_product_availability(product, quantity):
            messages.error(request, "Недостаточное количество товара на складе.")
            return redirect(
                request.META.get(
                    "HTTP_REFERER", reverse("product_detail", kwargs={"pk": pk})
                )
            )

        cart = request.session.get("cart", {})
        if pk in cart:
            if not check_product_availability(product, cart[pk]["quantity"] + quantity):
                messages.error(request, "Недостаточное количество товара на складе.")
                return redirect(
                    request.META.get(
                        "HTTP_REFERER", reverse("product_detail", kwargs={"pk": pk})
                    )
                )
            cart[pk]["quantity"] += quantity
        else:
            cart[pk] = {"quantity": quantity, "price": float(product.price)}

        request.session["cart"] = cart
        messages.success(request, "Товар добавлен в корзину.")
        return HttpResponseRedirect(
            request.META.get("HTTP_REFERER", reverse("product_list"))
        )


class CartView(View):

    def get(self, request):
        cart = request.session.get("cart", {})
        products = []
        total = 0
        for pk, details in cart.items():
            product = get_object_or_404(Product, pk=pk)
            total += details["quantity"] * details["price"]
            products.append(
                {
                    "product": product,
                    "quantity": details["quantity"],
                    "total_price": details["quantity"] * details["price"],
                }
            )

        return render(request, "cart/cart.html", {"products": products, "total": total})


class UpdateCartView(View):
    def post(self, request):
        cart = request.session.get("cart", {})

        for pk, item in cart.items():
            quantity = int(request.POST.get(f"quantity_{pk}", item["quantity"]))
            product = get_object_or_404(Product, pk=pk)

            if not check_product_availability(product, quantity):
                messages.error(
                    request,
                    f"Недостаточное количество товара {product.name} на складе.",
                )
            else:
                cart[pk]["quantity"] = quantity

        request.session["cart"] = cart
        messages.success(request, "Корзина обновлена.")
        return redirect("cart")


class CheckoutView(View):

    def get(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Ваша корзина пуста.")
            return redirect("cart")

        products = []
        total = 0
        for pk, details in cart.items():
            product = get_object_or_404(Product, pk=pk)
            if details["quantity"] > product.quantity:
                messages.error(
                    request, f"Недостаточное количество товара {product.name}."
                )
                return redirect("cart")
            total += details["quantity"] * product.price
            products.append(
                {
                    "product": product,
                    "quantity": details["quantity"],
                    "total_price": details["quantity"] * product.price,
                }
            )

        form = OrderForm()
        return render(
            request,
            "cart/checkout.html",
            {"products": products, "total": total, "form": form},
        )

    def post(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Ваша корзина пуста.")
            return redirect("cart")

        products = []
        total = 0
        for pk, details in cart.items():
            product = get_object_or_404(Product, pk=pk)
            if details["quantity"] > product.quantity:
                messages.error(
                    request, f"Недостаточное количество товара {product.name}."
                )
                return redirect("cart")
            total += details["quantity"] * product.price
            products.append(
                {
                    "product": product,
                    "quantity": details["quantity"],
                    "total_price": details["quantity"] * product.price,
                }
            )

        form = OrderForm(request.POST)
        if form.is_valid():
            # Сохраняем заказ
            order = form.save(commit=False)
            order.user = request.user
            order.created_at = timezone.now()
            order.save()
            order.products.set([item["product"] for item in products])
            order.save()

            for item in products:
                OrderDetail.objects.create(
                    order=order,
                    user=request.user,
                    order_number=order.id,
                    order_date=timezone.now(),
                    product=item["product"],
                    quantity=item["quantity"],
                    total_price=item["total_price"],
                    delivery_address=order.delivery_address,
                )

            for item in products:
                product = item["product"]
                product.quantity -= item["quantity"]
                product.save()

            messages.success(request, "Заказ успешно оформлен.")
            request.session["cart"] = {}
            return redirect("product_list")

        return render(
            request,
            "cart/checkout.html",
            {"products": products, "total": total, "form": form},
        )


class RepeatOrderView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        cart = request.session.get("cart", {})

        for product in order.products.all():
            product_id = str(product.id)
            if product_id in cart:
                cart[product_id]["quantity"] += 1
            else:
                cart[product_id] = {"quantity": 1, "price": float(product.price)}

        request.session["cart"] = cart
        messages.success(request, "Товары из заказа добавлены в корзину.")
        return redirect("cart")
