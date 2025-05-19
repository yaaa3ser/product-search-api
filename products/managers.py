from django.db import models
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q

class ProductManager(models.Manager):
    def search(self, query, category_id=None, brand_id=None):
        if not query:
            return self.none()

        query = query.strip().lower()
        
        vector = (
            SearchVector('name', weight='A', config='english') +
            SearchVector('name_ar', weight='A', config='arabic') +
            SearchVector('brand__name', weight='B', config='english') +
            SearchVector('brand__name_ar', weight='B', config='arabic') +
            SearchVector('category__name', weight='C', config='english') +
            SearchVector('category__name_ar', weight='C', config='arabic')
        )

        search_query = SearchQuery(query, config='english') | SearchQuery(query, config='arabic')

        # Calculate rank for full-text search
        rank = SearchRank(vector, search_query)

        # Trigram similarity for misspellings in both English and Arabic
        trigram_threshold = 0.2
        queryset = self.annotate(
            rank=rank,
            similarity_name=TrigramSimilarity('name', query),
            similarity_name_ar=TrigramSimilarity('name_ar', query)
        ).filter(
            Q(search_vector=search_query) |
            Q(similarity_name__gte=trigram_threshold) |
            Q(similarity_name_ar__gte=trigram_threshold)
        ).order_by('-rank', '-similarity_name', '-similarity_name_ar')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        return queryset