from django.urls import path

from customers.views import (ProfileView, 
                             AddressListView, AddressCreateView, 
                             AddressUpdateView, AddressDeleteView) 

app_name = 'customers'

urlpatterns = [
    path('profile/',ProfileView.as_view(), name="customer_profile"),
    path('address/',AddressListView.as_view(), name="customer_address_list"),
    path('address/create/',AddressCreateView.as_view(), name="customer_address_create"),
    path('address/edit/<int:pk>/',AddressUpdateView.as_view(), name="customer_address_edit"),
    path('address/delete/<int:pk>/',AddressDeleteView.as_view(), name="customer_address_delete"),
    path('order/',ProfileView.as_view(), name="customer_order"),
    path('order/detail/<int:pk>/',ProfileView.as_view(), name="customer_order_detail"),
    path('comment/',ProfileView.as_view(), name="customer_comment"),
    path('rate/',ProfileView.as_view(), name="customer_rate"),
]