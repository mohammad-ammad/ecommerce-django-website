from django.contrib import admin
from django.urls import path
from .views import index, signup, Login, products_details, logout, cart, checkout, ordersView
from .middlewares.auth import auth_middleware
urlpatterns = [
    path('', index, name='homepage'),
    path('signup',signup),
    path('login', Login.as_view(), name='login'),
    path('productsdetails/<int:pk>', products_details, name='productsdetails'),
    path('logout', logout),
    path('cart', cart, name="cart"),
    path('checkout', checkout, name="checkout"),
    path('orders', auth_middleware(ordersView), name="orders")
]
