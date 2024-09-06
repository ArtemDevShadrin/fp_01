from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from apps.catalog.models import Product


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        existing_review = Review.objects.filter(
            product=product, user=request.user
        ).first()
        if existing_review:
            messages.error(
                request,
                "Вы уже оставили отзыв на этот продукт. Вы можете обновить свой отзыв.",
            )
            return redirect("product_detail", pk=product_id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Ваш отзыв был добавлен.")
        else:
            messages.error(request, "Произошла ошибка. Пожалуйста, проверьте форму.")

        return redirect("product_detail", pk=product_id)


class ProductReviewsView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = product.reviews.all()
        return render(
            request,
            "reviews/product_reviews.html",
            {"product": product, "reviews": reviews},
        )
