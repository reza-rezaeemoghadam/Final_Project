# Importing needed Django built-in modules 
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 

# Importing Custome Forms
from accounts.forms import (CustomerRegisterForm, StaffRegisterForm,
                            LoginForm, StaffProfileForm, MarketEditForm) 
from website.forms import MarketForm

# Importing Models
from website.models import StaffMarkets, Markets
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
                       
class LoginView(FormView):
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
                                return redirect('accounts:dashboard_staff')
                            else:
                                return redirect('website:home_page')
                        messages.warning(request, "Entered informations were incorrect")
                    else:
                        messages.warning(request, "you haven't activated your account yet")
                else:
                    messages.warning(request, "Entered informations were incorrect")
        except Exception as error:
                        messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")

        context = {'login_form' : self.form}
        return render(request, self.template_name, context=context)
    
class CustomerPanelView(TemplateView):
    template_name = 'customer/customer_base.html'
        
class StaffPanelView(TemplateView):
    template_name="accounts/staff/staff_dashboard.html" 

class StaffProfileView(View):
    template_name="accounts/staff/staff_profile.html"   
    staff_form = StaffProfileForm
    market_form = MarketEditForm
    staff_model = User
    market_model = Markets
    
    def get(self, request):
        data = StaffMarkets.objects.filter(staff_id = request.user.id).first()
        if request.user.roll == 'Owner':            
            context = {'staff_form': self.staff_form(initial=data.staff.__dict__),
                       'market':self.market_form(initial=data.market.__dict__),
                       'img':data.staff.img,
                       'mar_id':data.market.id}
            return render(request, self.template_name ,context=context)
        else:
            context = {'staff_form': self.staff_form(initial=data.staff.__dict__),
                       'market':self.market_form(initial=data.market.__dict__),
                       'img':data.staff.img,
                       'read_only': True}
        return render(request, self.template_name, context=context)
    
    def post(self, request, pk):
        # try:
        edited_form = None
        if 'mar_btn' in request.POST:
            instance = self.market_model.objects.filter(id=pk).first()
            edited_form = self.market_form(request.POST, instance=instance)
            messages.success(request,'Address info successfully edited.')  
        elif 'acc_btn' in request.POST:
            instance = self.staff_model.objects.filter(pk=request.user.id).first()
            edited_form = self.staff_form(request.POST, instance=instance)
        if edited_form.is_valid():
            edited_form.save()  
            messages.success(request,'Your info successfully edited.')                  
        # except Exception as error:
        #     messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        return redirect("accounts:profile_staff")
