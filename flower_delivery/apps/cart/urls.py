from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartView,
    CheckoutView,
    RepeatOrderView,
)

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/<int:pk>/", AddToCartView.as_view(), name="add_to_cart"),
    path("update/", UpdateCartView.as_view(), name="update_cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("repeat/<int:order_id>/", RepeatOrderView.as_view(), name="repeat_order"),
]
