from rest_framework.generics import ListAPIView

# Importing Custome Models
from website.models import Categories

# Importing Custome Serializer
from .serializers import CategoryModelSerializer

class CategoryView(ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoryModelSerializer