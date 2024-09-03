from django import forms
from django.contrib.admin.widgets import AdminDateWidget

# Importing Custome Models
from website.models import Markets, Comments, Discounts

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
        
class AddComment(forms.ModelForm):
    class Meta:
        model = Comments   
        fields = ['title','text']     
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control rounded','placeholder':'Enter a title'})
        }
        
    def __init__(self, *args, **kwargs):
        super(AddComment, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={
            'class': 'form-control rounded',
            'id': 'textAreaExample',
            'row':'4'})


class DiscountForm(forms.ModelForm):
    
    class Meta:
        model = Discounts
        fields = ['dis_type', 'dis_amount', 'start_date', 'end_date']
        widgets = {
            'dis_type' : forms.Select(attrs={'class': 'form-control'}),
            'dis_amount' : forms.NumberInput(attrs={'class': "form-control mt-1", 'placeholder':'Enter the discount amount '}),
            'start_date' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter start date'}),
            'end_date' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter end date'})
        }