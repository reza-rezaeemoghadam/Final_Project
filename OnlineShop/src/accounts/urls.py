from django.urls import path

from .views import (CustomerRegisterView, StaffRegsiterView,
                    StaffPanelView, StaffProfileView,
                    LoginView, LogoutView)

app_name = "accounts"

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='register_customer'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/staff/', StaffRegsiterView.as_view(), name='register_owner'),
    path('dashboard-staff/', StaffPanelView.as_view(), name="dashboard_staff"),
    path('dashboard-staff/profile/', StaffProfileView.as_view(), name="profile_staff"),
    path('dashboard-staff/profile/<int:pk>', StaffProfileView.as_view(), name="profile_staff_edit"),
]