from rest_framework import serializers

# Importig Models
from website.models import Ratings, Products

# Implementing Serializers
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = "__all__"
                