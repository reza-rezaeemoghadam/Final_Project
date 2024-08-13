from django.db import models

from accounts.models import Customers, CustomerAddress
from website.models import Products

# Create your models here.
class Carts(models.Model):
    Customer = models.OneToOneField(Customers, related_name='cart', on_delete=models.CASCADE)

class CartDetails(models.Model):
    quantity = models.SmallIntegerField()
    cart = models.ForeignKey(Carts, related_name='cart_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)

class Orders(models.Model):
    date = models.DateTimeField()
    total_paid = models.IntegerField()
    shipment_status = models.CharField(max_length=20, default='در حال پردازش')
    shipment_date = models.DateTimeField()
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)
    address = models.ForeignKey(CustomerAddress, on_delete=models.DO_NOTHING)

class OrderDetails(models.Model):
    quantity = models.IntegerField()
    price = models.IntegerField()
    order = models.ForeignKey(Orders, on_delete=models.PROTECT, related_name="order_details")
    product = models.ForeignKey(Products, on_delete=models.RESTRICT)