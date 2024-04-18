from rest_framework import serializers

from orders.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'user_id',
            'crypto_currency_id',
            'crypto_currency_price',
            'count',
            'total_price',
            'paid_date',
            'is_settled'
        )
