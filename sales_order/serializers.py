from rest_framework import serializers
from .models import SalesOrder , SalesOrderLine ,StockMovementLog


class SalesOrderLineSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    available_stock = serializers.IntegerField(source='product.stock', read_only=True)

    class Meta:
        model = SalesOrderLine
        fields = ['product', 'product_name', 'qty', 'price', 'line_total', 'available_stock']
        read_only_fields = ['price', 'line_total', 'product_name', 'available_stock']

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
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            'order_number',
            'customer',
            'customer_name',
            'order_date',
            'created_by',
            'status',
            'total_amount',
            'lines'
        ]
        read_only_fields = [
            'order_number',
            'order_date',
            'created_by',
            'total_amount',
            'customer_name',
        ]

    def validate_status(self, value):
        """Prevent creating orders with non-pending status"""
        if not self.instance and value != SalesOrder.Status.PENDING:
            raise serializers.ValidationError(
                "New orders must be created with 'pending' status. Use PATCH to confirm."
            )
        return value

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

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)

        # Get new status if provided
        new_status = validated_data.get('status')

        # Validate status transition
        if new_status and new_status != instance.status:
            if new_status == SalesOrder.Status.CONFIRMED and instance.status != SalesOrder.Status.PENDING:
                raise serializers.ValidationError("Only pending orders can be confirmed")
            elif new_status == SalesOrder.Status.CANCELLED and instance.status != SalesOrder.Status.CONFIRMED:
                raise serializers.ValidationError("Only confirmed orders can be cancelled")

        # Update basic fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()  # This will trigger the save() method which handles status change

        # Update lines if provided
        if lines_data is not None:
            instance.lines.all().delete()
            for line_data in lines_data:
                SalesOrderLine.objects.create(order=instance, **line_data)
            instance.update_total()

        return instance


class StockMovementLogSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    action = serializers.SerializerMethodField()

    class Meta:
        model = StockMovementLog
        fields = [
            'id',
            'product',
            'product_name',
            'product_sku',
            'qty',
            'action',
            'user',
            'user_name',
            'timestamp'
        ]
        read_only_fields = fields

    def get_action(self, obj):
        return "Added to Stock" if obj.qty > 0 else "Removed from Stock"