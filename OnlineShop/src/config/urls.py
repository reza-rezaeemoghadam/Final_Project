"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('accounts/',include('accounts.urls')),
    path('customers/', include('customers.urls')),
    path('cart/', include('carts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/cart/', include('carts.api.v1.urls')),
    path('api/v1/customer/', include('customers.api.v1.urls')),
    path('api/v1/staff/', include('accounts.api.v1.urls')),
    path('api/v1/website/', include('website.api.v1.urls')),
]

admin.site.site_header = "Echo Shop Adminstration Page"
admin.site.site_title = "Echo|Admin Panel"
admin.site.index_title = "Welcome to the Echo Shop Adminstration Panel"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)