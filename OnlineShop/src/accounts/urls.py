from django.urls import path

from .views import CustomerRegisterView, StaffRegsiterView, Login

app_name = "accounts"

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='register_customer'),
    path('login/', Login.as_view(), name='login'),
    path('register/staff/', StaffRegsiterView.as_view(), name='register_owner'),
]