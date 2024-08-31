from django.urls import path,include

from .views import HomePageView, ProductDetailView, AddCommentView, ShopView, ShopProductView, SearchView

app_name = "website"

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    path('product/<int:pk>/add-comment', AddCommentView.as_view(), name="product_comment_create"),
    path('shop/', ShopView.as_view(), name="shop_list"),
    path('shop/<int:pk>', ShopProductView.as_view(), name="shop_detail"),
    path('search/', SearchView.as_view(), name="search"),
]