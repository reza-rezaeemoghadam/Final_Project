from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import os

from accounts.models import Customers, MarketAddress

# Create your models here.
class Markets(models.Model):
    market_name = models.CharField(max_length=100) 
    market_address = models.OneToOneField(MarketAddress, on_delete=models.DO_NOTHING)
    
class Categories(models.Model):
    title = models.CharField(max_length=60)
    parent = models.ForeignKey('Categories', on_delete=models.CASCADE)

class Discounts(models.Model):
    Percent = models
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    applied_by = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)   

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    discription = models.TextField()
    market = models.ManyToManyField(Markets, related_name='product')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='product')
    dicount = models.OneToOneField(Discounts, on_delete=models.SET_NULL, related_name='product')    
    
class ProductImages(models.Model): 
    image = models.ImageField(upload_to="images/product/", default="images/product/default.jpg")
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, related_name="image")

class Ratings(models.Model):
    rate = models.SmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='rating')
    customer = models.ForeignKey(Customers, default='not found', on_delete=models.SET_DEFAULT, related_name='rating')
    
class Comments(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    text = models.TextField()
    parent = models.ForeignKey('Comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comment')
    customer = models.ForeignKey(Customers, default='not found', on_delete=models.SET_DEFAULT, related_name='comment')     