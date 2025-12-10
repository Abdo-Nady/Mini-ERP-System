from rest_framework import serializers
from .models import SalesOrder
from .models import SalesOrderLine


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