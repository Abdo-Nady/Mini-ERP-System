from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'category',
            'cost_price',
            'selling_price',
            'stock',
            'image',
        ]
        read_only_fields = ['id']

    def validate_selling_price(self, value):
        """
        Ensure selling_price >= cost_price
        """
        cost_price = self.initial_data.get('cost_price')
        if cost_price is not None:
            cost_price = float(cost_price)
            if value < cost_price:
                raise serializers.ValidationError(
                    "Selling price cannot be less than cost price."
                )
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
