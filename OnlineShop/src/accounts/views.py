# Importing needed Django built-in modules 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages 

# Importing Custome Forms
from accounts.forms import CustomerRegisterForm, StaffRegisterForm, LoginForm
from website.forms import MarketForm

# Importing Models
from website.models import StaffMarkets 
from accounts.models import User

# Create your views here.
class CustomerRegisterView(View):
    template_name='accounts/register/register_customer.html' 
    model = User
    form = CustomerRegisterForm
    success_url = 'login'
    success_message = "your account has been registered successfully."
    
    def get(self, request):
        context = {'register_form':self.form()}        
        return render(request,self.template_name,context=context)
    
    # TODO: activation code
    def post(self, request):
        # try:
        register_form = self.form(request.POST)
        if register_form.is_valid():
            if not self.model.email_exist(request.POST.get('email')):
                register_form.save()
                messages.success(request, self.success_message)
            else:
                messages.warning(request, 'This email is already exists.')
        # except Exception as error:
        #     messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        
        context = {'register_form':self.form()}            
        return render(request, self.template_name, context=context)

class StaffRegsiterView(View):
    template_name='accounts/register/register_staff.html' 
    model = User
    register_form = StaffRegisterForm 
    market_form = MarketForm
    success_url = "accounts/login/"
    success_message = "your account has been registered successfully."
    
    def get(self, request):
        context = {'register_form' : self.register_form,
                   'market_form' : self.market_form}        
        return render(request,self.template_name,context=context)
    
    # TODO: impoelement something like transaction here
    # TODO: activation code
    def post(self, request):
        try:
            register_form = self.register_form(request.POST)
            market_form =  self.market_form(request.POST)
            if all([market_form.is_valid(), register_form.is_valid()]):
                if not self.model.email_exist(request.POST.get('email')):
                    owner = register_form.save()
                    market = market_form.save()
                    StaffMarkets.objects.create(staff=owner, market=market)
                    messages.success(request,self.success_message)
                else:
                    messages.warning(request,"This email is already exists")
        except Exception as error:
            messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        
        context = {'register_form' : self.register_form,
                   'market_form' : self.market_form}     
        return render(request, self.template_name, context=context)
                       
class Login(FormView):
    template_name='accounts/login/login.html' 
    model = User
    form = LoginForm
    
    def get(self, request):
        context = {'login_form' : self.form}
        return render(request, self.template_name, context=context) 
    
    def post(self, request):
        try:
            login_form = self.form(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = self.model.objects.filter(email__iexact=username).first()
                if user:
                    if user.is_active:
                        is_pass_correct = user.check_password(password)
                        if is_pass_correct:
                            login(request=request, user=user)
                            if user.is_staff:
                                pass
                            else:
                                return redirect(reverse('website:home_page'))
                        messages.warning(request, "Entered informations were incorrect")
                    else:
                        messages.warning(request, "you haven't activated your account yet")
                else:
                    messages.warning(request, "Entered informations were incorrect")
        except Exception as error:
                        messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")

        context = {'login_form' : self.form}
        return render(request, self.template_name, context=context)