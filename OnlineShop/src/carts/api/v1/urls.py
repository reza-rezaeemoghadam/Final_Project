from rest_framework.urls import path

from .views import (AddToCartAPIView, UpdateCartAPIView, CartCountAPIView, 
                    RemoveFromCartAPIView, CustomerAddressesAPIView, AddAddressAPIView, 
                    SubmitOrderAPIView, OrdersListAPIView)

urlpatterns = [
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('cart-count/', CartCountAPIView.as_view(), name='get_cart_count'),
    path('update-cart/', UpdateCartAPIView.as_view(), name='update_cart'),
    path('remove-cart/', RemoveFromCartAPIView.as_view(), name='remove_cart_item'),
    path('customer-addresses/', CustomerAddressesAPIView.as_view(), name='customer_addresses'),
    path('customer-addresses/add', AddAddressAPIView.as_view(), name='add_customer_addresses'),
    path('list-order/', OrdersListAPIView.as_view(), name='order_list'),
    path('submit-order/', SubmitOrderAPIView.as_view(), name='submit_order'),
]