from django.contrib import admin

from products.models import Product, Category, Brand

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'category')
    search_fields = ('name', 'brand__name', 'category__name')
    list_filter = ('brand', 'category')
    ordering = ('-id',)
    list_per_page = 20

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)
    list_per_page = 20

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)
    list_per_page = 20


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)