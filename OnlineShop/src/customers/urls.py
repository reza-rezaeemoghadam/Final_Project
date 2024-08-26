from django.urls import path

from customers.views import (ProfileView, 
                             AddressListView, AddressCreateView, 
                             AddressUpdateView, AddressDeleteView,
                             CommentListView, OrderList, OrderDetailView) 

app_name = 'customers'

urlpatterns = [
    path('profile/',ProfileView.as_view(), name="customer_profile"),
    path('address/',AddressListView.as_view(), name="customer_address_list"),
    path('address/create/',AddressCreateView.as_view(), name="customer_address_create"),
    path('address/edit/<int:pk>/',AddressUpdateView.as_view(), name="customer_address_edit"),
    path('address/delete/<int:pk>/',AddressDeleteView.as_view(), name="customer_address_delete"),
    path('order/',OrderList.as_view(), name="customer_order"),
    path('order/detail/<int:pk>/',OrderDetailView.as_view(), name="customer_order_detail"),
    path('comment/',CommentListView.as_view(), name="customer_comment_list"),
    path('comment/edit/<int:pk>',CommentListView.as_view(), name="customer_comment_edit"),
    path('comment/delete/<int:pk>',CommentListView.as_view(), name="customer_comment_delete"),
    path('rate/',ProfileView.as_view(), name="customer_rate"),
]