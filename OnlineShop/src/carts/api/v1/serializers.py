from rest_framework import serializers

from carts.models import Carts, Orders, OrderDetails
from website.models import Products
from accounts.models import CustomerAddress

class ProductSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'product_name', 'quantity', 'price', 'dicount', 'category']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ['id', 'created_at']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"        

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True)
    
    class Meta:
        model = Orders
        fields = "__all__"
        