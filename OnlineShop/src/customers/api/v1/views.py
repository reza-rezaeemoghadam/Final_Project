from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions
# Importing serializers
from .serializers import RatingSerializer
# Importing Models
from website.models import Ratings, Products

# Implementing Views
class RatingUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    def patch(self, request):
        user = request.user
        product = Products.objects.filter(id = request.data.get("product_id")).first()
        rate_val = request.data.get('rate')
        rate_obj = Ratings.objects.filter(customer = user, product = product).first()
        serializer = self.serializer_class(rate_obj, data = {'rate':rate_val}, partial = True)
        print(rate_val)
        print(request.data.get("product_id"))
        
class RatingSubmitAPIView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer
    queryset = Ratings.objects.all()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if (not pk) or (pk == '0'):
            user = request.user
            product = Products.objects.filter(id = request.GET.get("product_id")).first()
            rate_obj = Ratings.objects.filter(customer = user, product = product).first()
        else:
            rate_obj = Ratings.objects.filter(id = pk)
        if rate_obj: 
            serializer = self.serializer_class(data = rate_obj.__dict__)
            serializer.is_valid()             
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response({})
                
    def create(self, request, *args, **kwargs):
        user = request.user.id
        product = request.data.get('product_id')
        rate_val = request.data.get('rate')
        serializer = self.serializer_class(data = {"customer": user, "product": product, "rate": rate_val}) 
        if serializer.is_valid(raise_exception = False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    #TODO: for some reason this didnt work
    # def partial_update(self, request, *args, **kwargs):
    #     print("salam")
    #     return Response(status=status.HTTP_200_OK)
    
    # def update(self, request, *args, **kwargs):
    #     print("salam")
    #     return Response(status=status.HTTP_200_OK)
    