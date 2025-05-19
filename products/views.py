from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .models import Product
from .serializers import ProductSerializer

class ProductSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductSearchView(APIView):
    pagination_class = ProductSearchPagination

    def get(self, request):
        query = request.query_params.get('q', '')
        category_id = request.query_params.get('category_id')
        brand_id = request.query_params.get('brand_id')

        # Cache key based on query parameters
        cache_key = f"search:{query}:{category_id}:{brand_id}"
        cached_results = cache.get(cache_key)
        
        # if cached_results:
        #     return Response(cached_results)

        if not query:
            queryset = Product.objects.select_related('brand', 'category').all()
        else:
            # Perform search
            queryset = Product.objects.search(
                query=query,
                category_id=category_id,
                brand_id=brand_id
            ).select_related('brand', 'category')

        # Paginate results
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(page, many=True)

        # Cache results for 5 minutes
        response_data = paginator.get_paginated_response(serializer.data).data
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)