from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from apps.shop.models import Fruits
from .models import CartList
from ..coupon.models import Coupon


# Create your views here.

# VIEW CART
def cart(request):
    cpn = None
    total_price = 0
    if request.user.is_authenticated:
        # User is logged in
        cart_list = CartList.objects.filter(user=request.user)
        products = []
        count = 0
        for item in cart_list:
            products.append(item.fruit)
            products[count].quantity = item.quantity
            count += 1

        for product in products:
            product.total = product.price * product.quantity
            total_price += product.total

    else:
        # User is not logged in
        session_cart = request.session.get('cart', {})
        products = Fruits.objects.filter(id__in=session_cart.keys())
        # total_price = sum(product.price * session_cart[str(product.id)] for product in products)
        for product in products:
            product.quantity = session_cart[str(product.id)]
            product.total = product.price * product.quantity
            total_price += product.total
        actual_total_price = total_price
    try:
        session_coupon = request.session.get('coupon_id')
        now = timezone.now()
        cpn = Coupon.objects.get(id=session_coupon, valid_from__lte=now, valid_to__gte=now, active=True)
        cpn.amount = (total_price * cpn.discount) / 100
        actual_total_price = total_price - cpn.amount
    except Coupon.DoesNotExist:
        actual_total_price = total_price
    return render(request, 'cart.html',
                  {'products': products, 'total_price': total_price, 'actual_total_price': actual_total_price,
                   'coupon': cpn})


# ADD PRODUCT INTO CART
def add_to_cart(request, product_id):
    product = Fruits.objects.get(id=product_id)
    if request.user.is_authenticated:
        # User is logged in
        try:
            cart_item = CartList.objects.get(user=request.user, fruit=product)
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
            else:
                messages.info(request, "Quantity Limit Reached!")
                return redirect('cart')
            cart_item.save()
        except CartList.DoesNotExist:
            cart_item = CartList.objects.create(user=request.user, fruit=product)
            cart_item.save()
    else:
        # User is not logged in
        session_cart = request.session.get('cart', {})
        if session_cart.get(str(product_id), 0) < product.stock:
            session_cart[str(product_id)] = session_cart.get(str(product_id), 0) + 1
            request.session['cart'] = session_cart
    messages.success(request, "Cart Updated")
    return redirect('cart')


def cart_delete(request, product_id):
    if request.user.is_authenticated:
        item = CartList.objects.get(fruit=product_id, user=request.user)
        item.delete()
    else:
        session_cart = request.session.get('cart', {})

        if str(product_id) in session_cart:
            del session_cart[str(product_id)]
        request.session['cart'] = session_cart
    messages.success(request, "Product Removed Successfully")
    return redirect('cart')


# DECREMENT PRODUCT
def min_cart(request, product_id):
    if request.user.is_authenticated:
        item = CartList.objects.get(fruit=product_id, user=request.user)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    else:
        session_cart = request.session.get('cart', {})

        if str(product_id) in session_cart:
            if session_cart[str(product_id)] > 1:
                session_cart[str(product_id)] -= 1
            else:
                del session_cart[str(product_id)]
            request.session['cart'] = session_cart
    messages.success(request, "Cart Updated")
    return redirect('cart')
