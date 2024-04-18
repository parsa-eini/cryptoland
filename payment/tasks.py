from django.conf import settings
from django.utils import timezone
from django.db import transaction
from cryptoland.celery import app
from orders.models.order import Order
from payment.models import ExchangeSettlement


@app.task
def settlement_with_exchange():
    if settings.USE_PERIODIC_TASK:
        with transaction.atomic():
            not_settled_orders = Order.objects.select_for_update().filter(
                is_settled=False,
            ).values("id", "total_price")
            if not not_settled_orders.exists():
                return

            not_settled_settlement = ExchangeSettlement.objects.select_for_update().filter(
                state=ExchangeSettlement.STATE_PROCESSING,
                settlement_date__isnull=True
            ).order_by('created_date').first()
            if not not_settled_settlement:
                not_settled_settlement = ExchangeSettlement.objects.create(
                    state=ExchangeSettlement.STATE_PROCESSING,
                )

            not_settled_settlement.amount += sum([order["total_price"] for order in not_settled_orders])
            not_settled_settlement.orders.add(*[order["id"] for order in not_settled_orders])

            if not_settled_settlement.amount > settings.EXCHANGE_SETTLEMENT_MIN_AMOUNT:
                # call api
                not_settled_settlement.state = ExchangeSettlement.STATE_DONE
                not_settled_settlement.settlement_date = timezone.now()
                not_settled_settlement.save()
                not_settled_settlement.orders.update(is_settled=True)
