from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>', views.add_to_cart, name='addToCart'),
    path('delete/<int:product_id>', views.cart_delete, name='deleteCart'),
    path('min/<int:product_id>', views.min_cart, name='minCart')
]
