from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django .utils.translation import gettext_lazy as _
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
# we are using the PermissionsMixin here so that we can use written permissions and fetch them in the mean time
class User(AbstractUser, PermissionsMixin):
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
    
    def get_profile_url(self):
        return "/staff/dashboard/"
    
    #TODO: setting permissions on staffs
    def __set_permission(self, roll:str) -> None:
        """ Setting permissions base on staffs roll"""
        pass
    
    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        super().save(*args, **kwargs)
        

class Customers(User):
    class Meta:
        proxy = True
        
    def get_profile_url(self) -> str:
        return "/customer/dashboard/"
    
        
class CustomerAddress(models.Model):
    address = models.TextField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)
    customer = models.ForeignKey(Customers, null=True, blank=True, on_delete=models.CASCADE, related_name='addresses')
    
    class Meta:
        verbose_name = "آدرس مشتری"
        verbose_name_plural = "آدرس مشتریان"
    
    @classmethod
    def address_limit_reached(cls,customer_id) -> bool:
        count = cls.objects.filter(customer__id=customer_id).count()
        if count<3:
            return False
        return True


# permissions = [("complete_access", "Complete Access")]


# permissions = [("product_manipulation", "Product Manipulation"),
#                ("discount_manipulation", "Discount Manipulation"),
#                ("view_store_sections","View Store Sections")]
# permissions = [("view_store_sections","View Store Sections")]