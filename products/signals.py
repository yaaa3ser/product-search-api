from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Product

@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    # Fetch related fields
    brand_name = instance.brand.name if instance.brand else ''
    brand_name_ar = instance.brand.name_ar if instance.brand else ''
    category_name = instance.category.name if instance.category else ''
    category_name_ar = instance.category.name_ar if instance.category else ''

    # Construct SearchVector in Python
    search_vector = (
        SearchVector(models.Value(instance.name, output_field=models.TextField()), weight='A', config='english') +
        SearchVector(models.Value(instance.name_ar, output_field=models.TextField()), weight='A', config='arabic') +
        SearchVector(models.Value(brand_name, output_field=models.TextField()), weight='B', config='english') +
        SearchVector(models.Value(brand_name_ar, output_field=models.TextField()), weight='B', config='arabic') +
        SearchVector(models.Value(category_name, output_field=models.TextField()), weight='C', config='english') +
        SearchVector(models.Value(category_name_ar, output_field=models.TextField()), weight='C', config='arabic')
    )

    # Update the search_vector field
    Product.objects.filter(pk=instance.pk).update(search_vector=search_vector)


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete_pattern('search:*')  # Clear all search-related cache keys