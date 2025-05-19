from rest_framework import serializers
from .models import Product, Brand, Category

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'name_ar']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    rank = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'name_ar', 'brand', 'category', 'nutrition_facts', 'rank']