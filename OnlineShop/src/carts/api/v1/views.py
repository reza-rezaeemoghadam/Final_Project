from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from django.contrib import messages

import datetime
import json

from .serializers import ProductSerialzier, AddressSerializer, OrderSerializer, OrderDetailSerializer

from website.models import Products, ProductImages
from accounts.models import Customers, CustomerAddress
from carts.models import Orders, OrderDetails

def get_cart(request):
    cart = request.COOKIES.get('cart', None)
    if cart:
        cart = cart.replace('\'', '"')
        cart = json.loads(cart)
        return cart
    return None

class AddToCartAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerialzier
    model = Products
    image_model = ProductImages
    
    def post(self, request):
        pk = request.POST.get('pk')
        count = int(request.POST.get('count'))
        product = self.model.objects.get(id=pk)
        print(count)
        print(product.quantity)
        if count < product.quantity:
            cart = get_cart(request)
            pk = pk
            product_name = product.product_name
            price = product.price
            discount = "0"
            image = self.image_model.objects.filter(product_id=pk).first()
            discount = 0
            if product.dicount:
                discount = product.discount_calculation()
            if not cart:
                temp_cart = {pk : { "product_name" : product_name, "price": price, "count":count, "discount": discount, "image": image.image.url}}
                cart = f'{temp_cart}'
            else:
                if pk in cart:
                    cart[pk]["count"] += count
                else :
                    cart.update({pk : { "product_name" : product_name, "price": price, "count":count, "discount": discount, "image": image.image.url}})
            response = Response({'cart':'ok'})
            expire = datetime.datetime.now() + datetime.timedelta(weeks = 1)
            expire_string = expire.strftime("%a, %d-%b-%Y %H:%M:%S")
            response.set_cookie("cart", cart, expires=expire_string)
            response.data = {'cart_count': len(cart)}
            return response
        else:
            return Response({'product': 'not enough'}, status=HTTP_406_NOT_ACCEPTABLE)

class UpdateCartAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerialzier
    model = Products
    
    def get(self, request):
        cart = get_cart(request)
        if cart:
            return Response(cart)
        else:
            return Response({'cart': 'empty'})

class RemoveFromCartAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pk = request.GET.get('pk')
        cart = get_cart(request)
        cart.pop(pk)
        response = Response({'cart':'ok'})
        expire = datetime.datetime.now() + datetime.timedelta(weeks = 1)
        expire_string = expire.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("cart", cart, expires=expire_string)
        response.data = {'cart_count': len(cart)}
        return response

class CartCountAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        cart = get_cart(request)
        if cart:
            return  Response({'cart_count': len(cart)}, status=HTTP_200_OK)
        else:
          return Response({'cart_count': 0}, status=HTTP_200_OK)

class TotalPriceAPIView(APIView):
    permission_classes = [IsAuthenticated]

class OrdersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
        
class SubmitOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    model = Orders
    detail_model = OrderDetails
    request = None
    def clear_cookie(self, response):        
        response.delete_cookie('cart')
    
    def get_address(self):
        address_id = self.request.data['address_id']
        return CustomerAddress.objects.get(id=address_id)
    
    def get_shipment_date(self):
        shipping_method = self.request.data['shipping_method']
        if shipping_method == "Standard Delivery- €5.00":
            return (datetime.datetime.now() + datetime.timedelta(weeks=2)).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%S')
            
    def get_shipment_price(self):
        shipping_method = self.request.data['shipping_method']
        if shipping_method == "Standard Delivery- €5.00":
            return 5
        else:
            return 15  
    
    def get_user(self):
        return Customers.objects.get(id=self.request.user.id)
    
    def post(self, request):
        request =request
        address = self.get_address()
        shipping_price = self.get_shipment_price()
        shipment_date = self.get_shipment_date()
        user = self.get_user()
        cart = get_cart(request)
        total_price = shipping_price
        total_discount = 0
        details = []
        
        for key, val in cart.items():
            temp = {}
            product = Products.objects.get(id = key)
            temp['product'] = product
            temp['quantity'] = val['count']
            temp['price'] = val['price']
            temp['discount'] = val['discount'] * val['count']
            total_price += (val['price'] * val['count'])
            total_discount += (val['discount'] * val['count'])
            details.append(temp)
            product.quantity -= val['count']
            product.save()
                
        order = {'total_paid':total_price, 'total_discount':total_discount, 
                 'shipment_date':shipment_date, 'customer':user, 'address':address}

        order = self.model.objects.create(**order)
        
        for detail in details:
            self.detail_model.objects.create(order=order, **detail)
        
        response = Response(status=HTTP_200_OK)     
        self.clear_cookie(response)
        return response
            
                                   
                           

class CustomerAddressesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    model = CustomerAddress
    
    def get(self, request):
        pk = request.user.id
        addresses = self.model.objects.filter(customer_id = pk)
        if addresses:
            serializer = self.serializer_class(addresses, many=True)
            return Response(serializer.data)
        return Response({'cart':"empty"})

class AddAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    model = CustomerAddress   
    customer_model = Customers
    
    def get(self, request):
        addresses = self.model.objects.filter(customer_id=request.user.id)
        if len(addresses)>=3:
            messages.warning(request, "you have reached 3 address limit from your panel edit or delete one.")
        return Response({'address_count':len(addresses)})
    
    def post(self, request):
        customer = self.customer_model.objects.get(id = request.user.id)
        data = json.loads(request.data['address'])
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save(customer=customer)
        return Response(serializer.data, status=HTTP_200_OK) 