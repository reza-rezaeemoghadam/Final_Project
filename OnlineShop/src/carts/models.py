from django.db import models
from django.db.models import Count, Sum, F

# Importing Models
from accounts.models import Customers, CustomerAddress
from website.models import Products

# Importing Extra Modules
from datetime import datetime, timedelta

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

    @classmethod
    def get_total_income_last_n_days(cls, market, passed_days):
        days_ago = datetime.now() - timedelta(days=passed_days)

        total_income = cls.objects.filter(
            date__gte=days_ago,
            order_details__product__market=market
        ).aggregate(total_income=Sum('total_paid'))['total_income'] or 0

        return total_income

    @classmethod
    def count_returned_orders(cls, market):
        returned_orders_count = cls.objects.filter(
            shipment_status="Returned",
            order_details__product__market=market
        ).distinct().count()
        return returned_orders_count

    @classmethod
    def count_delivered_orders(cls, market):
        returned_orders_count = cls.objects.filter(
            shipment_status="Delivered",
            order_details__product__market=market
        ).distinct().count()
        return returned_orders_count
        
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
    
    @classmethod
    def get_total_market_sales(cls, market):
        total_sales = cls.objects.filter(
            product__market=market
        ).aggregate(total_sales=Sum(F('price') * F('quantity')))['total_sales'] or 0

        return total_sales
    
    @classmethod
    def sales_count_last_30_days(cls, market):
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)

        daily_sales = OrderDetails.objects.filter(
            order__date__gte=thirty_days_ago,
            product__market=market
        ).values('order__date__date').annotate(sales_count=Count('id')).order_by('order__date__date')
    
        return daily_sales
    
    @classmethod
    def get_top_best_selling_products(cls, market):
        top_products = cls.objects.filter(
            product__market=market
        ).values(
            'product__product_name'
        ).annotate(
            total_sales=Sum('quantity')
        ).order_by('-total_sales')[:6]    
        return top_products
    
    def __str__(self):
        return f"{self.order.id}--{self.product.product_name}" 