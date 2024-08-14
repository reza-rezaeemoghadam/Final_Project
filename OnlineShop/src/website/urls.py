from django.urls import path,include

from .views import HomePageView, ProductDetailView, AddCommentView

app_name = "website"

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    path('product/<int:pk>/add-comment', AddCommentView.as_view(), name="product_comment_create"),
]