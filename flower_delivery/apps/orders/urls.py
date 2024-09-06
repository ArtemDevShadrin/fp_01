from django.urls import path
from .views import (
    CreateOrderView,
    change_order_status,
    OrderDetailView,
    OrderListView,
    RepeatOrderView,
    OrderManagementView,
    OrderStatusUpdateView,
)

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create_order"),
    path("", OrderListView.as_view(), name="order_list"),
    path("repeat/<int:pk>/", RepeatOrderView.as_view(), name="repeat_order"),
    path("manage/", OrderManagementView.as_view(), name="order_management"),
    path(
        "manage/update/<int:pk>/",
        OrderStatusUpdateView.as_view(),
        name="update_order_status",
    ),
    path("detail/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("change_status/<int:pk>/", change_order_status, name="change_order_status"),
]
