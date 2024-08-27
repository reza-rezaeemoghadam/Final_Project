from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from accounts.models import Customers, Staffs

# Create your models here.
class Markets(models.Model):
    market_name = models.CharField(max_length=100) 
    address = models.TextField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاها"
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated_at = timezone.now()
        return super(Markets, self).save(*args, **kwargs)        
        
    def __str__(self):
        return f"{self.market_name}--{self.address}"

class StaffMarkets(models.Model):
    staff = models.OneToOneField(Staffs, on_delete=models.CASCADE, related_name='market')
    market = models.ForeignKey(Markets, on_delete=models.CASCADE, related_name='staff')
    
class Categories(models.Model):
    title = models.CharField(max_length=60)
    parent = models.ForeignKey('Categories', null=True, blank=True, on_delete=models.CASCADE)

class Discounts(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('value', 'Value'),
    ]
    dis_code = models.CharField(max_length=32, unique=True)
    dis_type = models.CharField(max_length=15, choices=DISCOUNT_TYPES, default="percentage")
    dis_amount = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    redeemed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    applied_by = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)   

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    market = models.ManyToManyField(Markets, related_name='product')
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, related_name='product')
    dicount = models.OneToOneField(Discounts, null=True, blank=True, on_delete=models.SET_NULL, related_name='product')   
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    @property
    def product_avg_rate(self) -> int:
        return Ratings.objects.filter(product_id=self.id).aggregate(avg_rating=Avg('rate'))['avg_rating']
    
    def discount_calculation(self):
        if self.dicount.dis_type == 'percentage':
            return (self.price * (self.dicount.dis_amount/100))
        elif self.dicount.dis_type == 'value':
            return 0
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated_at = timezone.now()
        return super(Products, self).save(*args, **kwargs)   
                
class ProductImages(models.Model): 
    image = models.ImageField(upload_to="images/product/", default="images/product/default.jpg")
    display_order = models.SmallIntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="image")

class Ratings(models.Model):
    rate = models.SmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='rating')
    customer = models.ForeignKey(Customers, default='not found', on_delete=models.SET_DEFAULT, related_name='rating')

    @classmethod
    def get_product_rate(cls, product_obj, customer_id):
        rate_val = cls.objects.filter(product=product_obj, customer__id = customer_id).first()
        if rate_val:
            return rate_val.rate
        return 0
    
class Comments(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    text = models.TextField()
    parent = models.ForeignKey('Comments', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comment')
    customer = models.ForeignKey(Customers, default='not found', on_delete=models.SET_DEFAULT, related_name='comment')     