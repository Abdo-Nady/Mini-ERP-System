from rest_framework import serializers
from .models import SalesOrder , SalesOrderLine ,StockMovementLog


class SalesOrderLineSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = SalesOrderLine
        fields = ['product', 'qty', 'price', 'line_total']

    def validate(self, data):
        product = data.get('product')
        qty = data.get('qty')

        if product and qty:
            if product.stock < qty:
                raise serializers.ValidationError({
                    'qty': f'Not enough stock for {product.name}. Available: {product.stock}, Requested: {qty}'
                })

        return data




class SalesOrderSerializer(serializers.ModelSerializer):
    lines = SalesOrderLineSerializer(many=True)
    total_amount = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = SalesOrder
        fields = ['order_number', 'customer', 'order_date', 'created_by', 'status', 'total_amount', 'lines']

    read_only_fields = [
        'order_number',
        'order_date',
        'created_by',
        'total_amount'
    ]

    def validate_lines(self, lines):
        """Validate all lines have sufficient stock"""
        if not lines:
            raise serializers.ValidationError("Order must have at least one line")

        errors = []
        for idx, line_data in enumerate(lines):
            product = line_data.get('product')
            qty = line_data.get('qty', 0)

            if product and qty > product.stock:
                errors.append({
                    'line': idx + 1,
                    'product': product.name,
                    'error': f'Not enough stock. Available: {product.stock}, Requested: {qty}'
                })

        if errors:
            raise serializers.ValidationError(errors)

        return lines

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        order = SalesOrder.objects.create(**validated_data)
        for line_data in lines_data:
            SalesOrderLine.objects.create(order=order, **line_data)
        order.update_total()
        return order



class StockMovementLogSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = StockMovementLog
        fields = ['id', 'product', 'product_name', 'qty', 'user', 'user_name', 'timestamp']
        read_only_fields = ['id', 'product_name', 'user_name', 'timestamp']
