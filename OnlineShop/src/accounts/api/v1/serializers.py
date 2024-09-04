from rest_framework import serializers

from carts.models import Orders

class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"