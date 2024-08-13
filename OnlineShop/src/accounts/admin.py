from django.contrib import admin

from .models import Customers,Staffs,CustomerAddress

# Register your models here.
admin.site.register(Customers)
admin.site.register(Staffs)
admin.site.register(CustomerAddress)