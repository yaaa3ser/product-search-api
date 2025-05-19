from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from .managers import ProductManager


class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, blank=True)  # Arabic name

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True)  # Arabic name
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutrition_facts = models.JSONField(default=dict, blank=True)
    search_vector = SearchVectorField(null=True)  # For full-text search
    
    objects = ProductManager()

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['name', 'name_ar']),  # For trigram similarity
        ]

    def __str__(self):
        return self.name


