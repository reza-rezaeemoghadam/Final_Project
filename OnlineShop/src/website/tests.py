from django.test import TestCase

# Importing Models
from accounts.models import Staffs, Customers
from website.models import Markets, Categories, Discounts, Products, ProductImages, Ratings, Comments

# Importing Extra Modules
from datetime import datetime, timedelta

# Create your tests here.
class WebsiteModelTest(TestCase):
    def setUp(self):
        # Accounts App Objects
        self.customer_set_up = Customers.objects.create(email="reza-customer@gmail.com",  password="123", first_name = "reza", last_name = "rezaee")
        self.customer_test = Customers.objects.create(email="reza-customer2@gmail.com",  password="123", first_name = "reza", last_name = "rezaee")
        self.staff = Staffs.objects.create(email="reza-staff@gmail.com",  password="123", first_name = "reza", last_name = "rezaee", roll = "Owner")
        # Website App Objects
        self.market = Markets.objects.create(market_name = "EchoShop", address = "Prirozi", state = "Tehran", city = "Tehran", postal_code = "19161728", telephone = "33333333")
        self.category = Categories.objects.create(title = "Laptop")
        self.product = Products.objects.create(product_name = "Asus G56", quantity = 25, description = "khili khobe", price = 85000000, category = self.category)
        self.product.market.add(self.market)
    
    def test_market(self):
        market = Markets.objects.create(market_name = "EchoShop2", address = "Prirozi", state = "Tehran", city = "Tehran", postal_code = "19161728", telephone = "33333333")
        
        self.assertTrue(isinstance(market, Markets))
        self.assertEqual(str(market), "EchoShop2--Prirozi")   
        self.assertNotEqual(market.created_at, None)
        self.assertNotEqual(market.updated_at, None)
        
    def test_category(self):
        category = Categories.objects.create(title = "PC")
        
        self.assertTrue(isinstance(category, Categories))
        self.assertEqual(str(category), "PC")   
    
    def test_discount(self):
        discount = Discounts.objects.create(dis_type = "Percentage", dis_amount = 20, start_date = datetime.now(), end_date = datetime.now()+timedelta(days=7), created_by = self.staff)

        self.assertTrue(isinstance(discount, Discounts))
        self.assertEqual(str(discount), "1--Percentage")   
        
    def test_product(self):
        product = Products.objects.create(product_name = "Asus G46", quantity = 46, description = "khili khobe", price = 75000000, category = self.category)
        product.market.add(self.market)
        
        self.assertTrue(isinstance(product, Products))
        self.assertEqual(str(product), "Asus G46--Laptop") 
        self.assertEqual(product.market.get(id=self.market.id), self.market)
        self.assertNotEqual(product.created_at, None)  
        self.assertNotEqual(product.updated_at, None)  
                
    def test_product_image(self):
        image = ProductImages.objects.create(display_order = 1, product = self.product)
        
        self.assertTrue(isinstance(image, ProductImages))
        self.assertEqual(str(image), "Asus G56") 
        self.assertEqual(image.product, self.product)
    
    def test_rating(self):
        rate = Ratings.objects.create(rate = 4, product = self.product, customer = self.customer_test)
        
        self.assertTrue(isinstance(rate, Ratings))
        self.assertEqual(str(rate), "reza--rezaee--Asus G56") 
        self.assertEqual(rate.product, self.product)
        self.assertEqual(rate.customer, self.customer_test)
        
    def test_comment(self):
        comment = Comments.objects.create(title = "Khili Khafane", text = "Config khili gavi dare", product = self.product, customer = self.customer_test)
        
        self.assertTrue(isinstance(comment, Comments))
        self.assertEqual(str(comment), "reza--rezaee--Asus G56") 
        self.assertEqual(comment.product, self.product)
        self.assertEqual(comment.customer, self.customer_test)
                