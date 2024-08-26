from django.shortcuts import render, redirect
from django.views.generic import View, DetailView

# Importing Custome Forms
from .forms import AddComment

# Importing Custome Models
from website.models import Products, Comments, ProductImages, Discounts
from accounts.models import User
from carts.models import Orders, OrderDetails 

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

class AddCommentView(View):
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