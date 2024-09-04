from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

# Importing Custome Permission
from accounts.permisssions import IsManagerMixin

# Importing Models
from carts.models import Orders

# Importing Serializers
from .serializers import OrderModelSerializer

class OrderUpdateAPIView(IsManagerMixin, UpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderModelSerializer
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
        