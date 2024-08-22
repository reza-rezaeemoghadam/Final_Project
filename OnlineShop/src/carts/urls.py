from django.urls import path

from carts.views import CartView, CartRegisterationView

app_name = "carts"

urlpatterns = [
    path('', CartView.as_view(), name="cart_list"),
    path('register/', CartRegisterationView.as_view(), name="cart_registration"),
]