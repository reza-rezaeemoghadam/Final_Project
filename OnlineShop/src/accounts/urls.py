from django.urls import path

from .views import (CustomerRegisterView, StaffRegsiterView, ProductAddView,
                    StaffPanelView, StaffProfileView, 
                    ProductListView, ProductDeleteView, ProductEditView,
                    DeleteImageView,
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
    path('dashboard-staff/products/', ProductListView.as_view(), name="profile_staff_product"),
    path('dashboard-staff/products/create/', ProductAddView.as_view(), name="profile_staff_product_create"),
    path('dashboard-staff/products/edit/<int:pk>/', ProductEditView.as_view(), name="profile_staff_product_edit"),
    path('dashboard-staff/products/delete/<int:pk>/', ProductDeleteView.as_view(), name="profile_staff_product_delete"),
    path('dashboard-staff/images/delete/', DeleteImageView.as_view(), name="profile_staff_image_delete"),
]