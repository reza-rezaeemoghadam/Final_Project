from django.urls import path, include
from rest_framework.routers import DefaultRouter 

from .views import RatingSubmitAPIView

rounter = DefaultRouter()
rounter.register("", RatingSubmitAPIView, basename="rate")

urlpatterns = [
    path("rate/", include(rounter.urls)),
]

 