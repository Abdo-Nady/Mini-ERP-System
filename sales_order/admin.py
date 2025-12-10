from django.contrib import admin
from .models import SalesOrder, SalesOrderLine, StockMovementLog

# Register your models here.

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer','order_date','created_by', 'status', 'total_amount']
    list_filter = ['status', 'order_date']

@admin.register(SalesOrderLine)
class SalesOrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'qty', 'price', 'line_total']
    list_filter = ['order', 'product']

@admin.register(StockMovementLog)
class StockMovementLogAdmin(admin.ModelAdmin):
    list_display = ['product', 'qty', 'user', 'timestamp']
    list_filter = ['product', 'user']