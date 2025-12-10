from django.contrib import admin
from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku','category','cost_price',    'selling_price', 'stock' ,'image']
    search_fields = ['name', 'sku' ,'category']