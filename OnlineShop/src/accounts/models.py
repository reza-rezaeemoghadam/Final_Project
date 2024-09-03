from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django .utils.translation import gettext_lazy as _
from django.contrib import admin
from django.template.defaultfilters import truncatechars 
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please provide an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email ,**extra_fields)
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

#TODO: There is some bugs when deleteing the user from Django Admin Panel
# It seems somehow it is related to your migrations later delete everything and try it
class User(AbstractUser):
    WEBSITE_ROLLS = [
        ("Owner","Owner"),
        ("Manager","Manager"),
        ("Operator","Operator"),
        ("Customer","Customer")             
    ]
    
    username = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    img = models.ImageField(upload_to="images/profile",default="images/profile/default.jpg")
    roll = models.CharField(max_length=30, choices=WEBSITE_ROLLS, default='Customer')
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = UserManager()    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    @classmethod
    def email_exist(cls, email:str) -> bool:
        return cls.objects.filter(email__iexact = email).exists()
    
    def get_profile_url(self):
        return "/profile/"
    
class Staffs(User):
    class Meta:
        proxy = True
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
    
    def get_profile_url(self):
        return "/staff/dashboard/"
    
    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name}--{self.last_name}"
        
class Customers(User):
    class Meta:
        proxy = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
                
    def get_profile_url(self) -> str:
        return "/customer/dashboard/"

    def __str__(self):
        return f"{self.first_name}--{self.last_name}"    
         
class CustomerAddress(models.Model):
    address = models.TextField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)
    customer = models.ForeignKey(Customers, null=True, blank=True, on_delete=models.CASCADE, related_name='addresses')
    
    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customers Address"
    
    @property
    @admin.display(description="address")
    def short_description(self):
        # this property defined for making the address character limited
        # in django admin panel
        return truncatechars(self.address, 20)
    
    @classmethod
    def address_limit_reached(cls,customer_id) -> bool:
        count = cls.objects.filter(customer__id=customer_id).count()
        if count<3:
            return False
        return True
    
    def __str__(self):
        return f"{self.id}--{self.customer.first_name}--{self.customer.last_name}"