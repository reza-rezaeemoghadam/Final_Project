from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

# Importing models
from carts.models import Orders, OrderDetails, Carts, CartDetails
# Register your models here.

@admin.register(Carts)
class CartAdmin(admin.ModelAdmin):
    list_display = ["view_cart_change_page", "view_customer_change_page", "created_at"]
    search_fields = ["customer__first_name", "customer__last_name"]
    list_filter = ['created_at']
    list_per_page = 10

    def view_cart_change_page(self, obj):
        # This method uses:
        # 1.Gain access the cart change page through this method
        url = (
            reverse("admin:carts_carts_change", args=[obj.id])
        )
        return format_html('<a href="{}">Cart ID:{}</a>', url, obj.id)        

    def view_customer_change_page(self, obj):
        # This method uses:
        # 1.Gain access to the customer change page 
        # 2.Customize the customer column 
        # 3.Display the first_name and last_name as it's link 
        url = (
            reverse("admin:accounts_customers_change", args=[obj.customer.id])
        )
        return format_html('<a href="{}">{} {}</a>', url, obj.customer.first_name, obj.customer.last_name)

    view_cart_change_page.short_description = "cart"
    view_customer_change_page.short_description = "customer"
    
@admin.register(CartDetails)
class CartDetailAdmin(admin.ModelAdmin):
    list_display = ["view_cart_detail_change_page", 'view_cart_change_page', 'view_product_change_page', 'quantity']
    search_fields = ['cart__id', 'cart__customer__first_name', 'cart__customer__last_name']
    list_per_page = 10
    
    def view_cart_detail_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object change page
        url = (
            reverse("admin:carts_cartdetails_change", args=[obj.id])
        )
        return format_html('<a href="{}">Detail: {}</a>', url, obj.id)
    
    def view_cart_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's cart change page
        url = (
            reverse("admin:carts_carts_changelist")
            +"?"
            + urlencode({"cart__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">Cart {}: {} {}</a>', url, obj.cart.id, obj.cart.customer.first_name, obj.cart.customer.last_name)

    def view_product_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's product change page 
        url = (
            reverse("admin:website_products_change" ,args=[obj.product.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.product_name)

    view_cart_detail_change_page.short_description = "cart detail"
    view_cart_change_page.short_description = "cart"
    view_product_change_page.short_description = "product"

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['view_order_change_page', 'view_customer_change_page', 'view_address_change_page', 'shipment_status', 'date', 'shipment_date']
    list_filter = ['shipment_status', 'date', 'shipment_date']
    search_fields = ["customer__first_name", "customer__last_name"]
    list_per_page = 10
    
    def view_order_change_page(self, obj):
        url = (
            reverse("admin:carts_orders_change", args=[obj.id])
        )
        return format_html('<a href="{}">Order ID:{}</a>', url, obj.id)        

    def view_customer_change_page(self, obj):
        # This method uses:
        # 1.Gain access to the customer change page 
        # 2.Customize the customer column 
        # 3.Display the first_name and last_name as it's link 
        url = (
            reverse("admin:accounts_customers_change", args=[obj.customer.id])
        )
        return format_html('<a href="{}">{} {}</a>', url, obj.customer.first_name, obj.customer.last_name)

    def view_address_change_page(self, obj):
        url = (
            reverse('admin:accounts_customeraddress_change', args=[obj.address.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.address.short_description)
    
    view_order_change_page.short_description = 'order'
    view_customer_change_page.short_description = "customer"
    view_address_change_page.short_description = 'address'

@admin.register(OrderDetails)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['view_order_detail_change_page', 'view_order_change_page', 'view_product_change_page', 'quantity']
    search_fields = ['order__id', 'order__customer__first_name', 'order__customer__last_name']
    list_per_page = 10
    
    def view_order_detail_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object change page
        url = (
            reverse("admin:carts_orderdetails_change", args=[obj.id])
        )
        return format_html('<a href="{}">Detail: {}</a>', url, obj.id)
    
    def view_order_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's order change page
        url = (
            reverse("admin:carts_orders_change", args=[obj.order.id])
        )
        return format_html('<a href="{}">Order {}: {} {}</a>', url, obj.order.id, obj.order.customer.first_name, obj.order.customer.last_name)

    def view_product_change_page(self, obj):
        # This method uses:
        # 1.Gain access to specified object's product change page 
        url = (
            reverse("admin:website_products_change" ,args=[obj.product.id])
        )
        return format_html('<a href="{}">{}</a>', url, obj.product.product_name)
    
    view_order_detail_change_page.short_description = "order detail"
    view_order_change_page.short_description = "order"
    view_product_change_page.short_description = "product"