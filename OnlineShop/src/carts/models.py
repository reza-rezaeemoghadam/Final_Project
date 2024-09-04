from django.db import models

from accounts.models import Customers, CustomerAddress
from website.models import Products

# Create your models here.
class Carts(models.Model):
    customer = models.OneToOneField(Customers, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"         

    def __str__(self):
        return f"{self.id}--{self.customer.first_name}--{self.customer.last_name}"

class CartDetails(models.Model):
    quantity = models.SmallIntegerField()
    cart = models.ForeignKey(Carts, related_name='cart_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name = "Cart Detail"
        verbose_name_plural = "Cart Details"           

    def __str__(self):
        return f"{self.cart.id}--{self.product.product_name}" 

class Orders(models.Model):
    SHIPMENT_STATUS = [
        ("Processing","Processing"),
        ("Delivering","Delivering"),
        ("Delivered","Delivered"),
        ("Returned","Returned")             
    ]
    
    date = models.DateTimeField(auto_now_add=True, editable=True)
    total_paid = models.IntegerField()
    total_discount = models.IntegerField()
    shipment_status = models.CharField(max_length=20, choices=SHIPMENT_STATUS, default='Processing')
    shipment_date = models.DateTimeField()
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)
    address = models.ForeignKey(CustomerAddress, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"  
        
    def __str__(self):
        return f"{self.id}--{self.customer.first_name}--{self.customer.last_name}"
     
class OrderDetails(models.Model):
    quantity = models.IntegerField()
    discount = models.IntegerField()
    price = models.IntegerField()
    order = models.ForeignKey(Orders, on_delete=models.PROTECT, related_name="order_details")
    product = models.ForeignKey(Products, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"     
    
    def __str__(self):
        return f"{self.order.id}--{self.product.product_name}" 