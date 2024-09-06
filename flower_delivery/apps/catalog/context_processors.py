from django.core.cache import cache


def cart_item_count(request):
    cart = request.session.get("cart", {})
    total_items = cache.get("cart_item_count")

    if total_items is None:
        total_items = sum(item["quantity"] for item in cart.values())
        cache.set("cart_item_count", total_items, 60)  # Кешируем на 60 секунд

    return {"cart_item_count": total_items}
