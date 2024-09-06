from django.urls import path
from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    LoadCartView,
    SaveCartView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("load-cart/", LoadCartView.as_view(), name="load_cart"),
    path("save-cart/", SaveCartView.as_view(), name="save_cart"),
]
