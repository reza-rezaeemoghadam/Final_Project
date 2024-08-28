from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

# Importing models
from .models import Customers,Staffs,CustomerAddress

# Register your models here.
@admin.register(Staffs)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email','roll', 'is_active']
    search_fields = ['first_name', 'last_name']
    list_filter = ['is_active', 'roll', 'date_joined']
    list_per_page = 10
    
    # We could have written this inside the model
    # but i've done it just for practice
    def full_name(self, obj):
        # This method uses:
        # 1.returns the full name of objects
        return f"{obj.first_name} {obj.last_name}"
    
    full_name.short_description = "name" 
    
@admin.register(Customers)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_active']
    search_fields = ['first_name', 'last_name']
    list_per_page = 10
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"    

    full_name.short_description = "name" 
    
@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['short_description', 'state','city', 'postal_code', 'view_customer_change_page'] 
    search_fields = ['customer__id', 'customer__first_name', 'customer__last_name']
    list_per_page = 10
    
    def view_customer_change_page(self, obj):
        # This method uses:
        # 1.Gain access to the customer change page 
        # 2.Customize the customer column 
        # 3.Display the first_name and last_name as it's link 
        url = (
            reverse("admin:accounts_customers_change", args=[obj.customer.id])
        )
        return format_html('<a href="{}">{} {}</a>', url, obj.customer.first_name, obj.customer.last_name)
    
    view_customer_change_page.short_description = "customer"