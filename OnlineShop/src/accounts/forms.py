from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

# Importing Custome Model
from accounts.models import Customers, Staffs
from website.models import Markets, Products, ProductImages, Discounts

# Customize Forms
class CustomerRegisterForm(forms.Form):
    MODEL = Customers
    first_name = forms.CharField(required=True,
                                label="First Name",
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your first name'}))
    
    last_name = forms.CharField(required=True,
                                label="Last Name",
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your last name'}))
   
    email = forms.EmailField(required=True,
                            label="Email",
                            widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'name@example.com'}),
                            validators=[validators.EmailValidator])
    
    password = forms.CharField(required=True,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Create a password'}))
    
    confirm_password = forms.CharField(required=True,
                                       label='Password Confirm',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm password'}))

    def save(self):
        try:            
            cleaned_data_copy = {}
            for key, value in self.cleaned_data.items():
                if key != 'password' and key != 'confirm_password':
                    cleaned_data_copy[key] = value
            password = self.clean_confirm_password()                                
            customer = self.MODEL(**cleaned_data_copy)              
            customer.set_password(password)
            customer.save()        
            return customer        
        except ValidationError:
            raise ValidationError()
            
    def clean_confirm_password(self):
        """ This function is used to check whether 
            the password and confirm_password are the same. """
            
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password == confirm_password:
            return confirm_password
        
        raise ValidationError('The passwords you entered dont match. Please try again')
    
class StaffRegisterForm(forms.ModelForm):     
    first_name = forms.CharField(required=True,
                                label="First Name",
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your first name'}))
    
    last_name = forms.CharField(required=True,
                                label="Last Name",
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your last name'}))
   
    email = forms.EmailField(required=True,
                            label="Email",
                            widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'name@example.com'}))
    

    password = forms.CharField(required=True,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter a password'}))
    
    confirm_password = forms.CharField(required=True,
                                       label='Password Confirm',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm password'}))

    class Meta:
        model = Staffs
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        # check wheter the email exist or not
        try:            
            cleaned_data_copy = {'roll':'Owner'}
            for key, value in self.cleaned_data.items():
                if key != 'password' and key != 'confirm_password':
                    cleaned_data_copy[key] = value
            password = self.clean_confirm_password()       
            # Creating staff object                     
            owner = self.Meta.model(**cleaned_data_copy)              
            owner.set_password(password)
            owner.save()        
            
            return owner        
        except ValidationError:
            raise ValidationError()
    
    def clean_confirm_password(self):
        """ This function is used to check whether 
            the password and confirm_password are the same. """
            
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password == confirm_password:
            return confirm_password
        
        raise ValidationError('The passwords you entered dont match. Please try again')
    
class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                                label="Username",
                                widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your username'}))    
    
    password = forms.CharField(required=True,
                           label='Password',
                           widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password'}))
    
    # remember_password =  

class StaffProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter your first name'}))    
    
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter your last name'}))  
    email = forms.EmailField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter your email',
                                                              'readonly':'readonly'}))  
    phone = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                          'placeholder':'Enter your phone'}))  
    img = forms.ImageField(required=True,
                           widget=forms.FileInput(attrs={'class':"form-control",
                                                         'onchange':"loadImages(event)"}))
    roll = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                          'placeholder':'Enter your roll',
                                                          'readonly':'readonly'}))  
    class Meta:
        model = Staffs
        fields = ['first_name','last_name','email','phone','img','roll']

class StaffForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True,
                                   label='Password Confirm',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm password'}))
    
    class Meta:
        model = Staffs
        fields = ['first_name','last_name','email','phone','img','roll', 'password',  'confirm_password']
        widgets = {
            'first_name' : forms.TextInput(attrs={'class': "form-control mt-1",
                                                  'placeholder':'Enter your first name'}),
            'last_name' : forms.TextInput(attrs={'class': "form-control mt-1",
                                                 'placeholder':'Enter your last name'}),
            'email' : forms.TextInput(attrs={'class': "form-control mt-1",
                                             'placeholder':'Enter your email'}),
            'phone' : forms.TextInput(attrs={'class': "form-control mt-1",
                                             'placeholder':'Enter your phone'}),
            'img' : forms.FileInput(attrs={'class':"form-control",
                                           'onchange':"loadImages(event)"}),
            'roll' : forms.Select(attrs={'class': "form-control mt-1",
                                            'placeholder':'Enter your roll'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter a password'})
        }
            
    def clean_confirm_password(self):
        """ This function is used to check whether 
            the password and confirm_password are the same. """
            
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password == confirm_password:
            return confirm_password
        
        raise ValidationError('The passwords you entered dont match. Please try again')        
        
class MarketEditForm(forms.ModelForm):
    
    market_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter your Market Name'}))
    
    address = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter the address'}))
    
    state = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter the state'}))
    
    city = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter the city'}))
    
    postal_code = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter the postal code'}))
    
    telephone = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control mt-1",
                                                              'placeholder':'Enter the phone'}))
    class Meta:
        model = Markets
        fields = ['market_name', 'address', 'state', 'city', 'postal_code', 'telephone']
    
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image']
        widgets = {
            'image' : forms.ClearableFileInput(attrs={'class': "form-control mt-1" , 'name': 'images', 'id': 'images', 'multiple': True}),
        }       
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'category', 'quantity', 'description', 'price', 'dicount']
        widgets = {
            'product_name' : forms.TextInput(attrs={'class': "form-control mt-1", 'placeholder':'Enter product name'}),
            'quantity' : forms.NumberInput(attrs={'class': "form-control mt-1", 'placeholder':'Enter quantity'}),
            'description' : forms.Textarea(attrs={'class': "form-control mt-1", 'placeholder':'Enter description'}),
            'category' : forms.Select(attrs={'class': "form-control mt-1"}),
            'price' : forms.NumberInput(attrs={'class': "form-control mt-1", 'placeholder':'Enter price'}),
            'dicount' : forms.Select(attrs={'class': "form-control mt-1"}),
        }

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discounts   
        fields = ['dis_type', 'dis_amount', 'start_date', 'end_date']
        widgets = {
            'dis_type' : forms.Select(attrs={'class': "form-control mt-1"}),
            'dis_amount' : forms.NumberInput(attrs={'class': "form-control mt-1", 'placeholder':'Enter the discount amount '}),
            'start_date' : forms.DateInput(attrs={'class': "form-control mt-1"}),
            'end_date' : forms.DateInput(attrs={'class': "form-control mt-1"}),                
        }