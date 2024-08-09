from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View, FormView

# Importing Custome Forms
from accounts.forms import CustomerRegisterForm, StaffRegisterForm, LoginForm
from website.forms import MarketForm

# Importing Models
from website.models import StaffMarkets 

# Create your views here.
class CustomerRegisterView(View, SuccessMessageMixin):
    template_name='register/customer_register.html' 
    success_url = 'login'
    form = CustomerRegisterForm
    success_message = "your account has been registered successfully."
    
    def get(self, request):
        context = {'register_form':self.form()}        
        return render(request,self.template_name,context=context)
    
    # TODO: activation code
    def post(self, request):
        register_form = self.form(request.POST)
        if register_form.is_valid():
            register_form.save()
        
        context = {'register_form':self.form()}    
        
        return render(request, self.template_name, context=context)

class StaffRegsiterView(View):
                                                                # First Approach with View
    template_name='register/staff_register.html' 
    success_url = "accounts/login/"
    register_form = StaffRegisterForm 
    market_form = MarketForm
    success_message = "your account has been registered successfully."
    
    def get(self, request):
        context = {'register_form' : self.register_form,
                   'market_form' : self.market_form}        
        return render(request,self.template_name,context=context)
    
    # TODO: impoelement something like trancaction here
    # TODO: activation code
    def post(self, request):
        register_form = self.register_form(request.POST)
        market_form =  self.market_form(request.POST)
        if all([market_form.is_valid(), register_form.is_valid()]):
            owner = register_form.save()
            market = market_form.save()
            st = StaffMarkets.objects.create(staff=owner, market=market)
            return render(request,self.success_url)
        
        context = {'register_form' : self.register_form,
                   'market_form' : self.market_form}     
        return render(request,self.template_name,context=context)
            
            
class Login(FormView):
    pass