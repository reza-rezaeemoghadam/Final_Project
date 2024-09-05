from rest_framework.urls import path

from .views import CategoryView

urlpatterns = [
    path('categories/list', CategoryView.as_view(), name='category_list')
]