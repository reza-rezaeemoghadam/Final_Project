from django.contrib import admin

from carts.models import Orders, OrderDetails
# Register your models here.
admin.site.register(Orders)
admin.site.register(OrderDetails)