from django.urls import path

from .views import (CustomerRegisterView, StaffRegsiterView,
                    StaffPanelView, CustomerPanelView,
                    StaffProfileView,
                    LoginView,)

app_name = "accounts"

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='register_customer'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/staff/', StaffRegsiterView.as_view(), name='register_owner'),
    path('dashboard-staff/', StaffPanelView.as_view(), name="dashboard_staff"),
    path('dashboard-customer/', CustomerPanelView.as_view(), name='dashboard_customer'),
    path('dashboard-staff/profile/', StaffProfileView.as_view(), name="profile_staff"),
    path('dashboard-staff/profile/<int:pk>', StaffProfileView.as_view(), name="profile_staff_edit"),
    path('dashboard-customer/profile/', CustomerPanelView.as_view(), name='profile_customer'),
]