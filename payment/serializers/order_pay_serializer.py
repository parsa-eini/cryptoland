from rest_framework import serializers


class OrderPaySerializer(serializers.Serializer):
    currency = serializers.CharField()
    count = serializers.IntegerField(min_value=1)
