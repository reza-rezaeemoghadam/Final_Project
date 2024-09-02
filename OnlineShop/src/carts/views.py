from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
# Create your views here.

class CartView(TemplateView):
    template_name = "website/cart_page.html"
    
class CartRegisterationView(LoginRequiredMixin, TemplateView):
    login_url = "accounts:login"
    template_name = "website/cart_submit.html"
    redirect_field_name = "next"