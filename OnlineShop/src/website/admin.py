from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

# Importing models
from website.models import StaffMarkets, Markets, Products, ProductImages, Categories, Discounts, Comments, Ratings

# Register your models here.
@admin.register(Markets)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['market_name', 'view_staff_change_list_page', 'created_at']
    list_filter = ['created_at']
    search_fields = ['market_name', 'staff__staff__first_name']

    def view_staff_change_list_page(self, obj):
        count = obj.staff.count()
        url = (
            reverse("admin:accounts_staffs_changelist")
            +"?"
            +urlencode({"market__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} staff</a>', url, count)
    
    view_staff_change_list_page.short_description = "staffs"

# TODO: This needs to get fixed
# @admin.register(StaffMarkets)
# class StaffMarketAdmin(admin.ModelAdmin):
#     pass

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'view_market_change_page', 'view_discount_change_page', 'price', 'created_at']
    list_filter = ['created_at', 'rating__rate']
    search_fields = ['product_name', 'market__market_name']
    
    def view_market_change_page(self, obj):
        count = obj.market.count()
        url = (
            reverse('admin:website_markets_changelist')
            +"?"
            +urlencode({"product__id":f"{obj.id}"})
        )    
        return format_html('<a href="{}">{} Market</a>', url, count)

    def view_discount_add_page(self, obj):
        url = (
            reverse('admin:website_discounts_add')            
        )
        return format_html('<a href="{}">Add Discount</a>', url)

    def view_discount_change_page(self, obj):
        if obj.dicount:
            sign = " %" if obj.dicount.dis_type == "percentage" else " "
            url = (
                reverse('admin:website_discounts_change', args=[obj.dicount.id])            
            )
            return format_html('<a href="{}">Discount:{}{}</a>', url, sign, obj.dicount.dis_amount)
        else:
            return self.view_discount_add_page(obj)

    view_market_change_page.short_description = "market"
    view_discount_change_page.short_description = "discount"
    
@admin.register(ProductImages)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['short_image_address', 'view_product_change_page', 'display_order']
    search_fields = ['product__product_name', 'display_order']
    list_per_page = 10
    
    def view_product_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's product change page 
        url = (
            reverse("admin:website_products_change" ,args=[obj.product.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.product_name)
    
    view_product_change_page.short_description = "product"

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'view_product_change_page', 'parent']
    search_fields = ['title']
    list_per_page = 10
    
    def view_product_change_page(self, obj):
        if obj.product:
            count = obj.product.count()
            url = (
                reverse("admin:website_products_changelist")
                +"?"
                +urlencode({"category__id": f"{obj.id}"})
            )
            return format_html('<a href="{}">{} Products</a>', url, count)

    view_product_change_page.short_description = "products"
    
@admin.register(Discounts)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['view_discount_change_page', 'view_product_change_page', 'view_staff_change_page', 'start_date', 'end_date', 'expired', 'redeemed']
    list_filter = ['redeemed', 'expired', 'start_date']
    search_fields = ['']
    list_per_page = 10

    def view_discount_change_page(self, obj):
        sign = " %" if obj.dis_type == "percentage" else " "
        url = (
            reverse('admin:website_discounts_change', args=[obj.id])            
        )
        return format_html('<a href="{}">Discount:{}{}</a>', url, sign, obj.dis_amount)

    def view_product_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's product change page 
        url = (
            reverse("admin:website_products_change" ,args=[obj.product.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.product_name)
    
    def view_staff_change_page(self, obj):
        # This method uses:
        # 1.Gain access to the staff change page 
        # 2.Customize the staff column 
        # 3.Display the first_name and last_name as it's link 
        url = (
            reverse("admin:accounts_staffs_change", args=[obj.applied_by.id])
        )
        return format_html('<a href="{}">{} {}</a>', url, obj.applied_by.first_name, obj.applied_by.last_name)

    view_product_change_page.short_description = "product"
    view_discount_change_page.short_description = "discount"
    view_staff_change_page.short_description = "applied by"

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_title', 'short_text', 'view_customer_change_page', 'view_product_change_page', 'date']
    list_filter = ['date']
    search_fields = ['product__id', 'product__product_name', 'customer__id', 'customer__first_name', 'customer__last_name']
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
    
    def view_product_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's product change page 
        url = (
            reverse("admin:website_products_change" ,args=[obj.product.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.product_name)
    
    view_product_change_page.short_description = "product"
    view_customer_change_page.short_description = "customer"  
    
@admin.register(Ratings)
class RateAdmin(admin.ModelAdmin):
    list_display = ['view_rate_change_page', 'view_product_change_page', 'view_customer_change_page', 'rate']
    search_fields = ['product__id', 'product__product_name', 'customer__id', 'customer__first_name', 'customer__last_name']
    list_filter = ['rate']
    list_per_page = 10    
    
    def view_rate_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's change page
        url = (
            reverse("admin:website_ratings_change", args=[obj.id])
        )
        return format_html('<a href="{}">Rating ID: {}</a>', url, obj.id)

    def view_customer_change_page(self, obj):
        # This method uses:
        # 1.Gain access to the customer change page 
        # 2.Customize the customer column 
        # 3.Display the first_name and last_name as it's link 
        url = (
            reverse("admin:accounts_customers_change", args=[obj.customer.id])
        )
        return format_html('<a href="{}">{} {}</a>', url, obj.customer.first_name, obj.customer.last_name)
    
    def view_product_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's product change page 
        url = (
            reverse("admin:website_products_change" ,args=[obj.product.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.product_name)
        
    view_rate_change_page.short_description = "rating"
    view_product_change_page.short_description = "product"
    view_customer_change_page.short_description = "customer"                   