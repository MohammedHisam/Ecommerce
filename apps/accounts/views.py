from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

from ..shop.models import Fruits
from ..cart.models import CartList


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('/')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect('/')
        elif password != confirm_password:
            messages.info(request, "Password not match!")
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registered Successfully :)")

            return redirect('/')
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully Logged out :)')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully Logged in :)')
            session_cart = request.session.get('cart')
            if session_cart:
                for product_id in session_cart:
                    try:
                        fruit = Fruits.objects.get(id=product_id)
                        item = CartList.objects.get(user=user, fruit=fruit)
                        item.quantity = session_cart[str(product_id)]
                        item.save()
                    except CartList.DoesNotExist:
                        cart_item = CartList.objects.create(user=request.user, fruit=fruit)
                        cart_item.save()
                messages.success(request, 'Cart Updated')
                request.session['cart'] = {}
            return redirect('/')
        else:
            messages.info(request, 'invalid details')
            return redirect('/')
    else:
        messages.info(request, "Login Required")
        return redirect('/')


