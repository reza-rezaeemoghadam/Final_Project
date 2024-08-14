from django.contrib import admin

from website.models import StaffMarkets, Markets, Products, ProductImages, Categories, Discounts, Comments

# Register your models here.
admin.site.register(Markets)
admin.site.register(StaffMarkets)
admin.site.register(Products)
admin.site.register(ProductImages)
admin.site.register(Categories)
admin.site.register(Discounts)
admin.site.register(Comments)