from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .models import Product
from apps.cart.models import Cart
from apps.reviews.models import Review
from apps.reviews.forms import ReviewForm


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["reviews"] = Review.objects.filter(product=product)
        context["form"] = ReviewForm()
        return context


class LoadCartView(View):

    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            request.session["cart"] = cart.items
        else:
            request.session["cart"] = request.session.get("cart", {})
        return redirect(reverse("cart"))


class SaveCartView(View):

    def post(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.items = request.session.get("cart", {})
            cart.save()
        return redirect(reverse("cart"))
