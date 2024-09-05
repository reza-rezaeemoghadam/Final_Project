# Importing needed Django built-in modules
from typing import Any
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView, ListView, CreateView
from django.views.generic.edit import DeleteView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Imporing Custome Permissions
from accounts.permisssions import IsOwnerMixin, IsManagerMixin, IsOperatorMixin, IsStaffMixin

# Importing customer Utils
from accounts.utils import send_otp_ghasedak

# Importing Extra Modules
import json

# Importing Custome Forms
from accounts.forms import (CustomerRegisterForm, StaffRegisterForm, ProductForm, ProductImageForm,
                            LoginForm, LoginPhoneForm, OTPForm, StaffProfileForm, StaffForm, MarketEditForm, CategoryForm)
from website.forms import MarketForm, DiscountForm

# Importing Models
from website.models import StaffMarkets, Markets, Products, ProductImages, Discounts, Categories
from accounts.models import User, Staffs
from carts.models import Orders, OrderDetails

# Create your views here.
class CustomerRegisterView(View):
    template_name = 'accounts/register/register_customer.html'
    model = User
    form = CustomerRegisterForm
    success_url = 'login'
    success_message = "your account has been registered successfully."

    def get(self, request):
        context = {'register_form': self.form()}
        return render(request, self.template_name, context=context)

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

        context = {'register_form': self.form()}
        return render(request, self.template_name, context=context)

class StaffRegsiterView(View):
    template_name = 'accounts/register/register_staff.html'
    model = User
    register_form = StaffRegisterForm
    market_form = MarketForm
    success_url = "accounts/login/"
    success_message = "your account has been registered successfully."

    def get(self, request):
        context = {'register_form': self.register_form,
                   'market_form': self.market_form}
        return render(request, self.template_name, context=context)

    # TODO: impoelement something like transaction here
    # TODO: activation code
    def post(self, request):
        try:
            register_form = self.register_form(request.POST)
            market_form = self.market_form(request.POST)
            if all([market_form.is_valid(), register_form.is_valid()]):
                if not self.model.email_exist(request.POST.get('email')):
                    owner = register_form.save()
                    market = market_form.save()
                    StaffMarkets.objects.create(staff=owner, market=market)
                    messages.success(request, self.success_message)
                else:
                    messages.warning(request, "This email is already exists")
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")

        context = {'register_form': self.register_form,
                   'market_form': self.market_form}
        return render(request, self.template_name, context=context)

class OTPVerificationView(FormView):
    template_name = "accounts/login/otp.html"
    form = OTPForm

    def get(self, request):
        context = {'login_form': self.form}
        return render(request, self.template_name, context=context) 
    
    def post(self, request):
        entered_key = request.POST.get('otp_key')       
        key = request.session.get('key')
        user_email = request.session.get('user_email')
        user = User.objects.get(email=user_email)
        if entered_key == key :
            if user.is_active:
                login(request=request, user=user)
                request.session.pop('user_email')
                request.session.pop('key')
                if user.is_staff:
                    return redirect('accounts:dashboard_staff')
                else:
                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    return redirect('website:home_page')
            else:
                messages.warning(request, "you haven't activated your account yet")
        messages.error(request, "Entered code is wrong")        
        return redirect('accounts:login_otp_verify')
        
class LoginPhoneView(FormView):
    template_name = "accounts/login/login_phone.html"
    model = User
    form = LoginPhoneForm
    
    def get(self, request):
        context = {'login_form': self.form}
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        phone_num = request.POST.get('phone_number')
        user = User.objects.filter(phone=phone_num).first()
        if user:
            res = send_otp_ghasedak(phone_num)
            if res:
                request.session['user_email'] = user.email
                request.session['key'] = res
                return redirect("accounts:login_otp_verify") 
            messages.error(request, "Somthing went wrong try another way")
            return redirect("accounts:login")  
        messages.error(request, "This phone number has not been registered")
        return redirect("accounts:login")  
     
class LoginView(FormView):
    template_name = 'accounts/login/login.html'
    model = User
    form = LoginForm

    def get(self, request):
        context = {'login_form': self.form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        try:
            login_form = self.form(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = self.model.objects.filter(
                    email__iexact=username).first()
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
                        messages.warning(
                            request, "Entered informations were incorrect")
                    else:
                        messages.warning(
                            request, "you haven't activated your account yet")
                else:
                    messages.warning(
                        request, "Entered informations were incorrect")
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")

        context = {'login_form': self.form}
        return render(request, self.template_name, context=context)


class StaffPanelView(IsStaffMixin, View):
    template_name = "accounts/staff/staff_dashboard.html"
    
    def get_context_data(self, request):
        market =request.user.market.market
        context = {}
        context['total_sale'] = OrderDetails.get_total_market_sales(market)
        context['last_month_sale'] = Orders.get_total_income_last_n_days(market,30)
        context ['count_returned_orders'] = Orders.count_returned_orders(market)
        context ['count_delivered_orders'] = Orders.count_delivered_orders(market)
        # context['top_sale'] = list(OrderDetails.get_top_best_selling_products(market))
        # context['every_day_sale_count'] = list(OrderDetails.sales_count_last_30_days(market))
        return context
    
    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data(request))    

class StaffProfileView(IsStaffMixin, View):
    template_name = "accounts/staff/staff_profile.html"
    staff_form = StaffProfileForm
    market_form = MarketEditForm
    staff_model = User
    market_model = Markets

    def get(self, request):
        data = StaffMarkets.objects.filter(staff_id=request.user.id).first()
        if request.user.roll == 'Owner':
            context = {'staff_form': self.staff_form(initial=data.staff.__dict__),
                       'market': self.market_form(initial=data.market.__dict__),
                       'img': data.staff.img,
                       'mar_id': data.market.id}
            return render(request, self.template_name, context=context)
        else:
            context = {'staff_form': self.staff_form(initial=data.staff.__dict__),
                       'market': self.market_form(initial=data.market.__dict__),
                       'img': data.staff.img,
                       'mar_id': data.market.id,
                       'read_only': True}
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        try:
            edited_form = None
            update = request.GET.get('update')
            match update:
                case "market":
                    if request.user.roll == "Owner":
                        instance = self.market_model.objects.filter(
                            id=pk).first()
                        edited_form = self.market_form(
                            request.POST, instance=instance)
                        messages.success(
                            request, 'Market info successfully edited.')
                    else:
                        messages.error(
                            request, "Access Denied you don't have the permission call admin for further action.")
                case "staff":
                    instance = self.staff_model.objects.filter(id=pk).first()
                    edited_form = self.staff_form(
                        request.POST, request.FILES, instance=instance)
                    messages.success(request, 'Your info successfully edited.')
                case _:
                    pass
            if edited_form.is_valid():
                edited_form.save()
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")
        finally:
            return redirect("accounts:profile_staff")

# TODO: Maybe adding logout confirmation


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
            if product_form.is_valid():
                self.form_valid(product_form, images)
            messages.success(request, "Product added successfully")
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")
        return redirect(reverse(self.success_url))

    def form_valid(self, product_form, images):
        counter = 0
        created_by = User.objects.get(id=self.request.user.id)
        market = StaffMarkets.objects.get(staff=created_by).market
        product = product_form.save()
        product.market.add(market)
        for image in images:
            counter += 1
            instance = self.image_model(
                product=product, image=image, display_order=counter)
            instance.save()


class ProductEditView(IsManagerMixin, View):
    model = Products
    image_model = ProductImages
    template_name = "accounts/staff/staff_product_update.html"
    success_url = "accounts:profile_staff_product"
    form_class = ProductForm
    image_form = ProductImageForm

    def get(self, request, pk):
        product = self.model.objects.get(id=pk)
        product_form = self.form_class(initial=product.__dict__)
        context = {'form': product_form,
                   'image_form': self.image_form, 'product': product}
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        instance = self.model.objects.get(id=pk)
        new_images = images = self.request.FILES.getlist('image')
        counter = len(new_images)
        edited_form = self.form_class(request.POST, instance=instance)
        product = edited_form.save()
        for image in images:
            counter += 1
            instance = self.image_model(
                product=product, image=image, display_order=counter)
            instance.save()
        return redirect(self.success_url)


class ProductDeleteView(IsManagerMixin, View):
    model = Products
    success_message = "Product deleted successfully."
    success_url = "accounts:profile_staff_product"

    def get(self, request, pk):
        self.model.objects.get(id=pk).delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)


class DeleteImageView(IsManagerMixin, View):
    model = ProductImages
    success_url = "accounts:profile_staff_product_edit"

    def post(self, request):
        image_id = request.POST.get('image')
        product_id = request.POST.get('product')
        self.model.objects.get(id=image_id).delete()
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
        # TODO:Fix this after market relation
        market_obj = StaffMarkets.objects.create(
            staff=self.object, market=self.request.user.market.market)
        return redirect(self.success_url)

# TODO: there is some bugs that i cant understnad here


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
        staff_obj = self.model.objects.get(id=pk)
        context = {
            'staff_form': self.form_class(initial=staff_obj.__dict__),
            'staff_id': staff_obj.id,
            'img': staff_obj.img,
            "edit": True
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            instance = self.model.objects.filter(id=pk).first()
            edited_form = self.form_class(
                request.POST, request.FILES, instance=instance)
            messages.success(request, 'Your info successfully edited.')
            if edited_form.is_valid():
                obj = edited_form.save(commit=False)
                obj.password = make_password(
                    edited_form.cleaned_data['password'])
                obj.save()
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")
        finally:
            return redirect(self.success_url)


class DiscountListView(IsManagerMixin, ListView):
    template_name = "accounts/staff/staff_discount_list.html"
    model = Discounts
    context_object_name = "discounts"

    def get_queryset(self):
        return self.model.objects.filter(created_by__market=self.request.user.market)


class DiscountAddView(IsManagerMixin, CreateView):
    template_name = "accounts/staff/staff_discount.html"
    success_url = "accounts:profile_discount_list"
    model = DiscountForm
    form_class = DiscountForm

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['discount_form'] = self.form_class
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.product = None
            obj.save()
        return redirect(self.success_url)


class DiscountDeleteView(IsManagerMixin, DeleteView):
    pass


class DiscountUpdateView(IsManagerMixin, View):
    template_name = "accounts/staff/staff_discount.html"
    success_url = "accounts:profile_discount_list"
    model = Discounts
    form_class = DiscountForm

    def get(self, request, pk):
        dis_obj = self.model.objects.get(id=pk)
        context = {
            'discount_form': self.form_class(initial=dis_obj.__dict__),
            'discount_id': dis_obj.id,
            "edit": True
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            instance = self.model.objects.filter(id=pk).first()
            edited_form = self.form_class(request.POST, instance=instance)
            messages.success(request, 'Your info successfully edited.')
            if edited_form.is_valid():
                edited_form.save()
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")
        finally:
            return redirect(self.success_url)


class OrdersView(IsManagerMixin, ListView):
    template_name = "accounts/staff/staff_order_list.html"
    model = Orders
    context_object_name = "orders"
    paginate_by = 10
    
    def get_queryset(self):
        products_in_market = Products.objects.filter(market=self.request.user.market.market)
        order_details_in_market = OrderDetails.objects.filter(product__in=products_in_market)
        return Orders.objects.filter(order_details__in=order_details_in_market).distinct()


class OrderDetailView(IsManagerMixin, ListView):
    template_name = "accounts/staff/staff_order_detail_list.html"
    model = OrderDetails
    context_object_name = "details"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for detail in context['details']:
            detail.total = (detail.price * detail.quantity) - (detail.discount* detail.quantity)
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(order__id = self.kwargs['pk'])

class CategoryListView(IsManagerMixin, ListView):
    template_name = "accounts/staff/staff_category_list.html"
    context_object_name = "categories"
    queryset = Categories.objects.all()
    paginate_by = 8

class CategoryAddView(IsManagerMixin, CreateView):
    template_name = "accounts/staff/staff_category.html"
    success_url = "accounts:profile_category_list"
    model = Categories
    form_class = CategoryForm

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['category_form'] = self.form_class
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.parent = None
            obj.save()
            messages.success(request, "Category Successfully Added")
        else:
            messages.error(request, "Category Addition Failed")
        return redirect(self.success_url) 

class CategoryUpdateView(IsManagerMixin, FormView):
    template_name = "accounts/staff/staff_category.html"
    success_url = "accounts:profile_category_list"
    model = Categories
    form_class = CategoryForm

    def get(self, request, pk):
        cat_obj = self.model.objects.get(id=pk)
        context = {
            'category_form': self.form_class(initial=cat_obj.__dict__),
            'category_id': cat_obj.id,
            "edit": True
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            instance = self.model.objects.filter(id=pk).first()
            edited_form = self.form_class(request.POST, instance=instance)
            messages.success(request, 'Your info successfully edited.')
            if edited_form.is_valid():
                edited_form.save()
        except Exception as error:
            messages.error(
                request, "An error occurred please check your entered info and if it occurred again contact support.")
        finally:
            return redirect(self.success_url)

    