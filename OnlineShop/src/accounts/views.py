# Importing needed Django built-in modules 
from typing import Any
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView, ListView, CreateView
from django.views.generic.edit import DeleteView 
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages 

# Imporing Custome Permissions
from accounts.permisssions import IsOwnerMixin, IsManagerMixin, IsOperatorMixin, IsStaffMixin

# Importing Custome Forms
from accounts.forms import (CustomerRegisterForm, StaffRegisterForm, ProductForm, ProductImageForm,
                            LoginForm, StaffProfileForm, StaffForm, MarketEditForm, DiscountForm) 
from website.forms import MarketForm

# Importing Models
from website.models import StaffMarkets, Markets, Products, ProductImages
from accounts.models import User, Staffs

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
                                if 'next' in request.GET:
                                    return redirect(request.GET['next'])
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
        
class StaffPanelView(IsStaffMixin,TemplateView):
    template_name="accounts/staff/staff_dashboard.html" 

class StaffProfileView(IsStaffMixin, View):
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
                       'mar_id':data.market.id,
                       'read_only': True}     
        return render(request, self.template_name, context=context)
    
    def post(self, request, pk):
        try:
            edited_form = None
            update = request.GET.get('update')
            match update:
                case "market":
                    if request.user.roll == "Owner":
                        instance = self.market_model.objects.filter(id=pk).first()
                        edited_form = self.market_form(request.POST, instance=instance)
                        messages.success(request,'Market info successfully edited.') 
                    else:
                        messages.error(request,"Access Denied you don't have the permission call admin for further action.") 
                case "staff":            
                    instance = self.staff_model.objects.filter(id=pk).first()
                    edited_form = self.staff_form(request.POST, request.FILES, instance=instance)
                    messages.success(request,'Your info successfully edited.')                  
                case _:
                    pass
            if edited_form.is_valid():
                edited_form.save()  
        except Exception as error:        
            messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        finally:
            return redirect("accounts:profile_staff")

#TODO: Maybe adding logout confirmation
class LogoutView(View):    
    def get(self, request):
        logout(request)
        return redirect('website:home_page') 
    
class ProductListView(IsStaffMixin, ListView):
    model = Products    
    template_name = 'accounts/staff/staff_product_list.html'
    context_object_name = "products"
    paginate_by = 8
    
    def get_queryset(self):
        return self.model.objects.filter(market=self.request.user.market.market)
    
class ProductAddView(IsManagerMixin, CreateView):    
    model = Products
    image_model = ProductImages
    success_url = "accounts:profile_staff_product_create"
    form_class = ProductForm
    image_form = ProductImageForm
    template_name = "accounts/staff/staff_product.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context["product_form"] = self.form_class
        context["image_form"] = self.image_form
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            product_form = self.form_class(request.POST)
            images = self.request.FILES.getlist('image')
            if product_form.is_valid() :
                self.form_valid(product_form, images)
            messages.success(request, "Product added successfully")
        except Exception as error:
            messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        return redirect(reverse(self.success_url))
        
    def form_valid(self, product_form, images):
            counter = 0
            created_by = User.objects.get(id = self.request.user.id )
            market = StaffMarkets.objects.get(staff = created_by).market
            product = product_form.save()
            product.market.add(market)
            for image in images:
                counter += 1            
                instance = self.image_model(product=product, image=image, display_order=counter)
                instance.save()
                
class ProductEditView(IsManagerMixin, View):
    model = Products
    image_model = ProductImages
    template_name = "accounts/staff/staff_product_update.html"
    success_url = "accounts:profile_staff_product"
    form_class = ProductForm
    image_form = ProductImageForm
    
    def get(self, request, pk):
        product = self.model.objects.get(id = pk)
        product_form = self.form_class(initial=product.__dict__)
        context = {'form':product_form , 'image_form' : self.image_form , 'product':product}
        return render(request, self.template_name, context=context)
    
    def post(self, request, pk):
        instance = self.model.objects.get(id = pk)
        new_images = images = self.request.FILES.getlist('image')
        counter = len(new_images)
        edited_form = self.form_class(request.POST, instance=instance)
        product = edited_form.save()
        for image in images:
            counter += 1            
            instance = self.image_model(product=product, image=image, display_order=counter)
            instance.save()
        return redirect(self.success_url)
        
class ProductDeleteView(IsManagerMixin, View):
    model = Products
    success_message = "Product deleted successfully."
    success_url = "accounts:profile_staff_product"
    
    def get(self, request, pk):
        self.model.objects.get(id = pk).delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
    
class DeleteImageView(IsManagerMixin, View):
    model = ProductImages   
    success_url = "accounts:profile_staff_product_edit"
    
    def post(self, request):
        image_id = request.POST.get('image')
        product_id = request.POST.get('product')
        self.model.objects.get(id = image_id).delete()
        return redirect(self.success_url, pk=product_id)
    
class StaffListView(IsStaffMixin, ListView):
    model = Staffs
    paginate_by = 10
    context_object_name = "staffs"
    template_name = "accounts/staff/staff_staff_list.html"
    
    def get_queryset(self):
        market = self.request.user.market
        staff_markets = StaffMarkets.objects.filter(market=market.market)
        return [staff_market.staff for staff_market in staff_markets]
    
class StaffAddView(IsOwnerMixin, CreateView):
    model = Staffs
    form_class = StaffForm
    template_name = "accounts/staff/staff_staff.html"
    success_url = "accounts:profile_staff_list"
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)    
        context['staff_form'] = self.form_class
        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        #TODO:Fix this after market relation
        market_obj = StaffMarkets.objects.create(staff=self.object, market=self.request.user.market.market)
        return redirect(self.success_url)

#TODO: there is some bugs that i cant understnad here    
class StaffDeleteView(IsOwnerMixin, View):
    success_url = "accounts:profile_staff_add"
    model = Staffs
    
    def get(self, request, *args, **kwargs):
        # obj = StaffMarkets.objects.get(staff__id = self.kwargs['pk'])
        # obj.delete()
        staff_obj = self.model.objects.filter(id=self.kwargs['pk']).first()
        print(staff_obj)
        staff_obj.delete()
        messages.success("Selected Staff Deleted Successfully!")
        return redirect(self.success_url)

class StaffUpdateView(IsOwnerMixin, View):
    model = Staffs
    form_class = StaffForm
    template_name = "accounts/staff/staff_staff.html"
    success_url = "accounts:profile_staff_list"
    
    def get(self, request, pk):
        staff_obj = self.model.objects.get(id = pk)
        context = {
            'staff_form' : self.form_class(initial=staff_obj.__dict__),
            'staff_id' : staff_obj.id,
            'img' : staff_obj.img,
            "edit" : True
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        # try:       
        instance = self.model.objects.filter(id=pk).first()
        edited_form = self.form_class(request.POST, request.FILES, instance=instance)
        messages.success(request,'Your info successfully edited.')                  
        if edited_form.is_valid():
            edited_form.save()  
        # except Exception as error:        
        messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        # finally:
        return redirect(self.success_url)        