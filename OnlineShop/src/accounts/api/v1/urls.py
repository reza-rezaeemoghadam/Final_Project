from rest_framework.urls import path

from .views import OrderUpdateAPIView

urlpatterns = [
    path('order_shipment_update/<int:pk>/', OrderUpdateAPIView.as_view(), name="order_shipment_update")
]