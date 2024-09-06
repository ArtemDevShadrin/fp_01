from django.urls import path
from .views import AddReviewView, ProductReviewsView

urlpatterns = [
    path(
        "product/<int:product_id>/add_review/",
        AddReviewView.as_view(),
        name="add_review",
    ),
    path(
        "product/<int:product_id>/reviews/",
        ProductReviewsView.as_view(),
        name="product_reviews",
    ),
]
