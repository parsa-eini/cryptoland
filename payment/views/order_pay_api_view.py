from django.db.models import F
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, get_object_or_404
from currencies.models import CryptoCurrency
from orders.models.order import Order
from orders.serializers import OrderSerializer
from payment.serializers import OrderPaySerializer
from django.db.transaction import atomic


class OrderPayAPIView(APIView):
    serializer_class = OrderPaySerializer
    read_serializer_class = OrderSerializer

    @atomic
    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        wallet = user.wallet
        currency = get_object_or_404(CryptoCurrency, name=validated_data['currency'])
        count = validated_data['count']

        total_amount = currency.price * count

        if wallet.balance < total_amount:
            raise ValidationError(detail={"balance": "Not enough balance"})

        wallet.balance = F('balance') - total_amount
        wallet.save()

        order = Order.objects.create(
            user=user,
            crypto_currency=currency,
            crypto_currency_price=currency.price,
            count=count,
            total_price=total_amount,
            paid_date=timezone.now(),
            is_settled=False
        )
        return Response(
            self.read_serializer_class(instance=order).data,
            status=status.HTTP_201_CREATED
        )
