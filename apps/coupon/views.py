from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon


# Create your views here.


@require_POST
def coupon(request):
    now = timezone.now()
    code = request.POST.get('coupon')
    try:
        cpn = Coupon.objects.get(code__iexact=code,
                                 valid_from__lte=now,
                                 valid_to__gte=now,
                                 active=True)
        request.session['coupon_id'] = cpn.id
        messages.success(request, "Coupon Applied")
    except Coupon.DoesNotExist:
        request.session['coupon_id'] = None
        messages.warning(request, "Invalid Coupon")
    return redirect('cart')
