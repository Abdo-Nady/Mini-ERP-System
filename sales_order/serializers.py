from rest_framework import serializers
from .models import SalesOrder , SalesOrderLine ,StockMovementLog


class SalesOrderLineSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = SalesOrderLine
        fields = ['product', 'qty', 'price', 'line_total']

class SalesOrderSerializer(serializers.ModelSerializer):
    lines = SalesOrderLineSerializer(many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = SalesOrder
        fields = ['order_number', 'customer', 'order_date', 'created_by', 'status', 'total_amount', 'lines']

class StockMovementLogSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = StockMovementLog
        fields = ['id', 'product', 'product_name', 'qty', 'user', 'user_name', 'timestamp']
        read_only_fields = ['id', 'product_name', 'user_name', 'timestamp']
