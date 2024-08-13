from django import forms

from website.models import Markets

class MarketForm(forms.ModelForm):
    
    market_name = forms.CharField(max_length=100,
                                  required=True,
                                  label="Market Name",
                                  widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your market name'}))
    
    address = forms.CharField(required=True,
                              label="Address",
                              widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Enter the address of your market'}))
    
    state = forms.CharField(required=True,
                            label="State",
                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter the state of your market'}))
    
    
    city = forms.CharField(required=True,
                            label="City",
                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter the city of your market'}))
    
    postal_code = forms.CharField(required=True,
                            label="Postal Code",
                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter the postal code of your market'}))
    
    
    class Meta:
        model = Markets
        fields = ['market_name', 'address', 'state', 'city', 'postal_code']