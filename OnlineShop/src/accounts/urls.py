from django.urls import path

from .views import (CustomerRegisterView, StaffRegsiterView, ProductAddView,
                    StaffPanelView, StaffProfileView, StaffListView, StaffAddView, StaffDeleteView, StaffUpdateView,
                    ProductListView, ProductDeleteView, ProductEditView,
                    CategoryListView, CategoryAddView, CategoryUpdateView,
                    DiscountListView, DiscountAddView, DiscountDeleteView, DiscountUpdateView,
                    OrdersView, OrderDetailView,
                    DeleteImageView,
                    LoginView, LoginPhoneView, OTPVerificationView, LogoutView)

app_name = "accounts"

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='register_customer'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/phone', LoginPhoneView.as_view(), name='login_phone'),
    path('login/phone/verify/', OTPVerificationView.as_view(), name='login_otp_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/staff/', StaffRegsiterView.as_view(), name='register_owner'),
    path('dashboard-staff/', StaffPanelView.as_view(), name="dashboard_staff"),
    path('dashboard-staff/profile/', StaffProfileView.as_view(), name="profile_staff"),
    path('dashboard-staff/profile/<int:pk>', StaffProfileView.as_view(), name="profile_staff_edit"),
    path('dashboard-staff/staff/add/', StaffAddView.as_view(), name="profile_staff_add"),
    path('dashboard-staff/staff/list/', StaffListView.as_view(), name="profile_staff_list"),
    path('dashboard-staff/staff/update/<int:pk>/', StaffUpdateView.as_view(), name="profile_staff_update"),
    path('dashboard-staff/staff/delete/<int:pk>/', StaffDeleteView.as_view(), name="profile_staff_delete"),
    path('dashboard-staff/products/', ProductListView.as_view(), name="profile_staff_product"),
    path('dashboard-staff/products/create/', ProductAddView.as_view(), name="profile_staff_product_create"),
    path('dashboard-staff/products/edit/<int:pk>/', ProductEditView.as_view(), name="profile_staff_product_edit"),
    path('dashboard-staff/products/delete/<int:pk>/', ProductDeleteView.as_view(), name="profile_staff_product_delete"),
    path('dashboard-staff/images/delete/', DeleteImageView.as_view(), name="profile_staff_image_delete"),
    path('dashboard-staff/discount/list/', DiscountListView.as_view(), name="profile_discount_list"),
    path('dashboard-staff/discount/add/', DiscountAddView.as_view(), name="profile_discount_add"),
    path('dashboard-staff/discount/delete/<int:pk/', DiscountDeleteView.as_view(), name="profile_discount_delete"),
    path('dashboard-staff/discount/update/<int:pk>/', DiscountUpdateView.as_view(), name="profile_discount_update"),
    path('dashboard-staff/order/list/', OrdersView.as_view(), name="profile_order_list"),
    path('dashboard-staff/order/<int:pk>/detail/', OrderDetailView.as_view(), name="profile_order_detail"),
    path('dashboard-staff/category/list/', CategoryListView.as_view(), name="profile_category_list"),
    path('dashboard-staff/category/add/', CategoryAddView.as_view(), name="profile_category_add"),
    path('dashboard-staff/category/<int:pk>/update/', CategoryUpdateView.as_view(), name="profile_category_update"),
]