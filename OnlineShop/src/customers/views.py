from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
# Importing Custome Forms
from customers.forms import CustomerProfileForm, CustomerAddressForm
# Importing Models
from accounts.models import User, CustomerAddress
from website.models import Comments
# Create your views here.
class ProfileView(View):
    template_name = "accounts/customer/customer_profile.html"
    template_form = CustomerProfileForm
    model = User
    
    def get(self, request):
        initial_form_data = self.model.objects.filter(id=request.user.id).first()
        context = {'customer_form': self.template_form(initial=initial_form_data.__dict__),
                   'img':initial_form_data.img}
        return render(request, self.template_name, context=context)

    def post(self, request):
        try:
            data = self.model.objects.filter(id=request.user.id).first()
            edited_form = self.template_form(request.POST, request.FILES, instance=data)
            if edited_form.is_valid():
                edited_form.save()
                messages.success(request, "Your info successfully edited.")
        except Exception as error:
                messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        return redirect("customers:customer_profile")
    
class AddressListView(ListView):
    template_name = 'accounts/customer/customer_address_list.html'
    context_object_name = 'addresses'
    model = CustomerAddress
    
    def get_qeuryset(self):
        user_id = self.request.user.id
        print(self.model.objects.filter(customer_id = user_id))
        return self.model.objects.filter(customer_id = user_id)

class AddressCreateView(CreateView):
    model_class = CustomerAddress
    template_name = "accounts/customer/customer_address.html"
    form_class = CustomerAddressForm
    success_url = "customers:customer_address_list"
    
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["customer_address"] = self.get_form()
            kwargs['create'] = True
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):        
        if not self.model_class.address_limit_reached(request.user.id): 
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            messages.warning(request, 'You have reached address limit insertion please edit or remove the previous ones.')
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        try:
            user_date = User.objects.get(id=request.user.id)    
            form = self.form_class(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.customer = user_date
                obj.save()
                messages.success(request, "Address info successfully added.")
        except Exception as error:
                messages.error(request, "An error occurred please check your entered info and if it occurred again contact support.")        
        return redirect(self.success_url)
       
class AddressUpdateView(View):
    model = CustomerAddress
    template_name = "accounts/customer/customer_address.html"
    form_class = CustomerAddressForm
    success_url = "customers:customer_address_list"
    
    def get_context_data(self, **kwargs) -> dict:
        kwargs['update'] = True
        return kwargs

    def get_query_set(self, pk):
        return self.model.objects.get(id=pk)

    def get(self, request, pk):
        queryset = self.get_query_set(pk)
        context = {'customer_address' : self.form_class(initial=queryset.__dict__),
                   'address_id': queryset.id}
        print(self.get_context_data(**context))
        return render(request, self.template_name, context=self.get_context_data(**context))
        
    def post(self, request, pk):
        # try:
        address_instance = self.model.objects.get(id=pk)
        user_instance = User.objects.get(id=request.user.id)    
        form = self.form_class(request.POST, instance=address_instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = user_instance
            obj.save()
            messages.success(request, "Address info successfully edited.")
        # except Exception as error:
        #         messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")        
        return redirect(self.success_url)
    
class AddressDeleteView(View):
    model = CustomerAddress
    success_message = "Address deleted successfully."
    
    def get(self, request, pk):
        try:
            obj = self.model.objects.get(id=pk)        
            obj.delete()        
            messages.success(self.request, self.success_message) 
        except Exception as error:
            messages.error(request,"An error occurred please check your entered info and if it occurred again contact support.")
        return redirect("customers:customer_address_list")
    
class CommentListView(ListView):
    template_name = "accounts/customer/customer_comment_list.html"
    model = Comments
    paginate_by = 10
    context_object_name = "comments"
         