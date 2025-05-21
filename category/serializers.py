from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    name=serializers.Serializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name']