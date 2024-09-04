from django.test import TestCase, Client
from django.urls import reverse

# Importing Models
from accounts.models import Staffs, Customers, CustomerAddress

# Create your tests here.
class AccountModelTest(TestCase):
    def setUp(self):
        self.customer = Customers.objects.create(email="reza-customer@gmail.com", password="123", first_name = "reza", last_name = "rezaee")
        
        self.staff = Customers.objects.create(email="reza-staff@gmail.com", password="123", first_name = "reza", last_name = "rezaee", roll = "Owner")
     
    def test_staff(self):
        staff = Staffs.objects.create(email="reza-test-staff@gmail.com", password="123", roll = "Owner", first_name = 'reza', last_name = "rezaee")
        
        self.assertEqual(str(staff), 'reza--rezaee')
        self.assertTrue(isinstance(staff, Staffs))
        self.assertTrue(staff.is_staff)
                    
    def test_customer(self):
        customer = Customers.objects.create(email="reza-test-customer@gmail.com", password="123", first_name = 'reza', last_name = "rezaee")
        
        self.assertEqual(str(customer), 'reza--rezaee')
        self.assertTrue(isinstance(customer, Customers))
        self.assertEqual(customer.roll, "Customer")
            
    def test_customer_address(self):
        address = CustomerAddress.objects.create(address = "Pirozi", state = "Tehran", city = "Tehran", postal_code = "19161728", customer = self.customer)
        
        self.assertEqual(address.customer, self.customer)
        self.assertEqual(str(address), "1--reza--rezaee")
        self.assertTrue(isinstance(address, CustomerAddress))
    
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("accounts:login")
        self.staff = Customers.objects.create(email="reza-staff@gmail.com", password="123", first_name = "reza", last_name = "rezaee", roll = "Owner")
        self.customer = Customers.objects.create(email="reza-test-customer@gmail.com", password="123", first_name = 'reza', last_name = "rezaee")

    def test_can_access_login_page(self):
        response = self.client.get(self.login_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login/login.html")

    def test_successful_login(self):
        response = self.client.post(self.login_url, {'username': 'reza-staff@gmail.com' , 'password': '123'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login/login.html")                

class OwnerRegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_register_url = reverse("accounts:register_owner")

    def test_can_access_login_page(self):
        response = self.client.get(self.staff_register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register/register_staff.html")    

    def test_successful_login(self):
        response = self.client.post(self.staff_register_url, {'first_name': 'Reyhane' , 
                                                              'last_name': 'Ebrahimian', 
                                                              'email': 'reyhane@gmail.com', 
                                                              'password' : '123', 
                                                              'confirm_password' : '123'})
    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register/register_staff.html")    

class CustomerRegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_register_url = reverse("accounts:register_customer")

    def test_can_access_login_page(self):
        response = self.client.get(self.customer_register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register/register_customer.html")    

    def test_successful_login(self):
        response = self.client.post(self.customer_register_url, {'first_name': 'Reyhane' , 
                                                              'last_name': 'Ebrahimian', 
                                                              'email': 'reyhane22@gmail.com', 
                                                              'password' : '123', 
                                                              'confirm_password' : '123'})
    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register/register_customer.html")    