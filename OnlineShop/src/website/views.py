from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, DetailView


# Importing Custome Forms
from .forms import AddComment
# Importing Custome Models
from website.models import Products, Comments, ProductImages
from accounts.models import User 
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'website/website_home.html'

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