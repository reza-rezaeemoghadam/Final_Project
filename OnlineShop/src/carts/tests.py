from django.test import TestCase

# Importing Models 
from accounts.models import Staffs, Customers, CustomerAddress
from carts.models import Carts, CartDetails, Orders, OrderDetails
from website.models import Products, Categories, Markets
# Importing Extra Classes
import datetime

# Create your tests here.
class CartModelTest(TestCase):
    def setUp(self):
        # Accounts App Objects
        self.customer_set_up = Customers.objects.create(email="reza-customer@gmail.com",  password="123", first_name = "reza", last_name = "rezaee")
        self.customer_test = Customers.objects.create(email="reza-customer2@gmail.com",  password="123", first_name = "reza", last_name = "rezaee")
        self.address = CustomerAddress.objects.create(address = "Pirozi", state = "Tehran", city = "Tehran", postal_code = "19161728", customer = self.customer_set_up)
        self.staff = Staffs.objects.create(email="reza-staff@gmail.com",  password="123", first_name = "reza", last_name = "rezaee", roll = "Owner")
        # Carts App Objects
        self.cart = Carts.objects.create(customer=self.customer_set_up)
        self.order = Orders.objects.create(customer=self.customer_set_up, total_paid = 120000, total_discount = 30000, shipment_date = datetime.datetime.now(), address = self.address)
        # Website App Objects
        self.market = Markets.objects.create(market_name = "EchoShop", address = "Prirozi", state = "Tehran", city = "Tehran", postal_code = "19161728", telephone = "33333333")
        self.category = Categories.objects.create(title = "Laptop")
        self.product = Products.objects.create(product_name = "Asus G56", quantity = 25, description = "khili khobe", price = 85000000, category = self.category)
        self.product.market.add(self.market)
        
    def test_cart(self):
        cart = Carts.objects.create(customer = self.customer_test)
        
        self.assertTrue(isinstance(cart, Carts))
        self.assertEqual(str(cart), "2--reza--rezaee")
    
    def test_cart_detail(self):
        detail = CartDetails.objects.create(cart=self.cart, quantity = 3, product = self.product)
        
        self.assertTrue(isinstance(detail, CartDetails))
        self.assertEqual(str(detail), "1--Asus G56")
    
    def test_order(self):
        orders = Orders.objects.create(customer = self.customer_test, total_paid = 120000, total_discount = 30000, shipment_date = datetime.datetime.now(), address = self.address)
        
        self.assertTrue(isinstance(orders, Orders))
        self.assertEqual(str(orders), "2--reza--rezaee")
        
    def test_order_detail(self):
        detail = OrderDetails.objects.create(quantity = 5, discount = 12000000, price = 85000000, order = self.order, product = self.product)
        
        
        self.assertTrue(isinstance(detail, OrderDetails))
        self.assertEqual(str(detail), "1--Asus G56")