from django.contrib.auth.models import BaseUserManager,AbstractUser,PermissionsMixin
from django .utils.translation import gettext_lazy as _
from django.db import models

import os

from website.models import Markets

# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please provide an email address")
        
        email = self.normalize_email(email) 
        user = self.model(email=email **extra_fields)
        # Hashes the password through set_password and within it make_password hasher from django.contrib.auth.hashers 
        user.set_password(password)     
        user.save()
        return user
                    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields) 

# we are using the PermissionsMixin here so that we can use written permissions and fetch them in the mean time
class User(AbstractUser, PermissionsMixin):
    class WebsiteRolls(models.TextChoices):
        OWNER = "Owner",_("Owner")
        MANAGER = "Manager",_("Manager")
        OPERATOR = "Operator",_("Operator")
        CUSTOMER =  "Customer",_("Customer")      
    
    #TODO: find a structure for this purpose
    def get_file_path(instance, filename):
        return os.path.join("images/profile/",instance.id,filename)
    
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=16)
    img = models.ImageField(upload_to="images/profile",default="images/profile/default.jpg")
    roll = models.CharField(max_length=30, choices=WebsiteRolls.choices, default=WebsiteRolls.CUSTOMER)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['email', 'password']
    
    def get_profile_url(self):
        return "/profile/"
    
class Staffs(User):
    class Meta:
        proxy = True
    
    def get_profile_url(self):
        return "/staff/dashboard/"
        

class Customers(User):
    class Meta:
        proxy = True
        
    def get_profile_url(self):
        return "/customer/dashboard/"


class StaffMarkets(models.Model):
    staff = models.OneToOneField(Staffs, on_delete=models.CASCADE, related_name='market')
    market = models.ForeignKey(Markets, on_delete=models.CASCADE, related_name='staff')


class AddressBase(models.Model):
    address = models.TextField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)

    class Meta:
        abstract = True
        
class CustomerAddress(AddressBase):
    customer = models.ForeignKey(Customers, null=True, blank=True, on_delete=models.CASCADE, related_name='addresses')
    
    class Meta:
        proxy = True

class MarketAddress(AddressBase):
    class Meta:
        proxy = True
           
# permissions = [("complete_access", "Complete Access")]


# permissions = [("product_manipulation", "Product Manipulation"),
#                ("discount_manipulation", "Discount Manipulation"),
#                ("view_store_sections","View Store Sections")]
# permissions = [("view_store_sections","View Store Sections")]