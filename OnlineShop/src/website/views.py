from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from django.db.models import Sum, Avg
# Importing Custome Forms
from .forms import AddComment

# Importing Custome Models
from website.models import Products, Comments, ProductImages, Discounts, Markets
from accounts.models import User
from carts.models import OrderDetails 

# Create your views here.
class HomePageView(View):
    product_model = Products
    order_detail_model =  OrderDetails
    template_name = 'website/website_home.html'
    
    def get_queryset(self):
        # Top 8 sales
        # product_quantities = OrderDetails.objects.values('product').annotate(total_quantity=Sum('quantity'))
        # most_sold_product = product_quantities.order_by('-total_quantity')[:8]
        # Top 8 Discount Products
        discount_product = Discounts.objects.filter(expired=False).select_related('product')
        # all Product
        most_sold_product = self.product_model.objects.all()
        return {'most_sold_products':most_sold_product, 'discount_products':discount_product}

    def get(self, request):
        return render(request, self.template_name, context=self.get_queryset())
    
class ProductDetailView(DetailView):
    model = Products
    comment_model = Comments
    context_object_name = "product"
    template_name = 'website/product_detail.html'

class AddCommentView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "next"
    comment_model = Comments
    product_model = Products
    customer_model = User
    image_model = ProductImages
    template_name = 'website/product_comment.html'
    form_class = AddComment
    success_url = 'website:product_detail'
    
    def get_queryset(self, pk):
        return  self.image_model.objects.get(product_id=pk, display_order=1), self.product_model.objects.get(id=pk)
    
    def get(self, request, pk):
        image , product = self.get_queryset(pk)
        context = {'comment_form' : self.form_class,
                   'image' : image,
                   'product': product}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.customer = self.customer_model.objects.get(id = request.user.id)
            comment.product = self.product_model.objects.get(id =pk)
            comment.save()
            return redirect('website:product_detail', pk=pk)
        
        
class ShopView(ListView):
    model = Markets
    context_object_name = 'shops'
    template_name = 'website/shop_page.html'    
    paginate_by = 2
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        sort_by =self.request.GET.get('sortBy')
        sort_type = self.request.GET.get('Type') 
        if sort_by and sort_type:
            context['sortBy'] = sort_by
            context['Type'] = sort_type
        return context
        
    def get_queryset(self):
        sort_type = self.request.GET.get('Type')
        if sort_type == 'asc':
            sort_type = '+'
        else:
            sort_type = '-'
            
        sort_by = self.request.GET.get('sortBy')
        match sort_by:
            case 'date':
                return self.model.objects.all().order_by(f"{sort_type}created_at")
            case 'highest_score':
                markets_with_avg_rating = self.model.objects.annotate(avg_product_rating=Avg('product__rating__rate')).order_by(f"{sort_type}avg_product_rating")  
                return markets_with_avg_rating
            case 'most_sell':
                markets_with_sales = self.model.objects.annotate(total_quantity_sold=Sum('product__orderdetails__quantity')).order_by(f"{sort_type}total_quantity_sold")                
                return markets_with_sales
            case _: 
                return self.model.objects.all()


class ShopProductView(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'website/product_list_page.html'    
    paginate_by = 2
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        sort_by =self.request.GET.get('sortBy')
        sort_type = self.request.GET.get('Type') 
        context['market_pk'] = self.kwargs['pk']
        if sort_by and sort_type:
            context['sortBy'] = sort_by
            context['Type'] = sort_type
        return context
    
    def get_queryset(self):
        shop_pk = self.kwargs['pk']
        sort_type = self.request.GET.get('Type')
        if sort_type == 'asc':
            sort_type = ''
        else:
            sort_type = '-'
        
        sort_by = self.request.GET.get('sortBy')
        match sort_by:
            case 'date':
                return self.model.objects.all().order_by(f"{sort_type}created_at").filter(market__id = shop_pk)
            case 'highest_score':
                return self.model.objects.annotate(avg_product_rating=Avg('rating__rate')).order_by(f"{sort_type}avg_product_rating").filter(market__id = shop_pk)  
            case 'most_sell':
                return self.model.objects.annotate(total_quantity_sold=Sum('orderdetails__quantity')).order_by(f"{sort_type}total_quantity_sold").filter(market__id = shop_pk)
            case 'price':
                return self.model.objects.order_by(f"{sort_type}price").filter(market__id = shop_pk)
            case _: 
                return self.model.objects.filter(market__id = shop_pk)
        
    
class SearchView(ListView):
    product_model = Products
    market_model = Markets
    template_name = "website/website_search_result.html"
    context_object_name = None
    paginate_by = 8
    
    def get_queryset(self):
        search_by = self.request.GET.get('search_by') 
        print(search_by)
        q = self.request.GET.get('q')
        print(q)
        match search_by:
            case "shop":
                self.context_object_name = "shops"
                print(self.market_model.objects.filter(market_name__icontains = q))
                return self.market_model.objects.filter(market_name__icontains = q)
            case "product":
                self.context_object_name = "products"
                print(self.product_model.objects.filter(product_name__icontains = q))
                return self.product_model.objects.filter(product_name__icontains = q)
            case __:
                pass    
    