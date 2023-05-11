from .models import CartList


def count(request):
    item_count = 0
    items = []
    if 'admin' in request.path:
        return {}
    else:
        if request.user.is_authenticated:
            cart_item = CartList.objects.filter(user=request.user)
            for item in cart_item:
                item_count += item.quantity
                items.append(item.fruit_id)
        else:
            session_cart = request.session.get('cart', {})
            for item in session_cart:
                item_count += session_cart[item]
                items.append(int(item))
    return dict(item_count=item_count, items=items)
