from django import forms

from accounts.models import Customers, CustomerAddress

class CustomerProfileForm(forms.ModelForm):
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
    
    class Meta:
        model = Customers
        fields = ['first_name', 'last_name', 'email', 'phone', 'img']

#TODO: if this worked implement it on the other forms        
class CustomerAddressForm(forms.ModelForm):
    
    class Meta:
        model = CustomerAddress
        fields = ['address', 'state', 'city', 'postal_code']
        widgets = {
            'address': forms.Textarea(attrs={'class': "form-control mt-1",'placeholder':'Enter the address'}),
            'state' :  forms.TextInput(attrs={'class': "form-control mt-1",'placeholder':'Enter the state'}),
            'city' :   forms.TextInput(attrs={'class': "form-control mt-1",'placeholder':'Enter the city'}),
            'postal_code' : forms.TextInput(attrs={'class': "form-control mt-1",'placeholder':'Enter the postal code'})
        }
