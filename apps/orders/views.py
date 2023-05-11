from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from ..coupon.models import Coupon
from ..cart.models import CartList


# Create your views here.

@login_required
def checkout(request):
    cart_list = CartList.objects.filter(user=request.user)
    products = []
    total_price = 0
    count = 0
    for item in cart_list:
        products.append(item.fruit)
        products[count].quantity = item.quantity
        count += 1

    for product in products:
        product.total = product.price * product.quantity
        total_price += product.total

    try:
        session_coupon = request.session.get('coupon_id')
        now = timezone.now()
        cpn = Coupon.objects.get(id=session_coupon, valid_from__lte=now, valid_to__gte=now, active=True)
        cpn.amount = (total_price * cpn.discount) / 100
        actual_total_price = total_price - cpn.amount
    except Coupon.DoesNotExist:
        actual_total_price = total_price
    return render(request, 'checkout.html',
                  {'products': products, 'total_price': total_price, 'actual_total_price': actual_total_price,
                   'coupon': cpn})
