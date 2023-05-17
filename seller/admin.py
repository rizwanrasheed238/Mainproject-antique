from django.contrib import admin
from .models import seller_product

class SellerProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'price', 'category', 'stock']
    list_filter = ['name', 'category']
    search_fields = ['user__username', 'product__name']

# admin.site.register(seller_product, SellerProductAdmin)