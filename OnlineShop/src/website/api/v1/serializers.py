from rest_framework import serializers

# Importing Custome Model
from website.models import Categories

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"