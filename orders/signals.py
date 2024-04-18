from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from orders.models.order import Order
from payment.models import ExchangeSettlement


@receiver(post_save, sender=Order)
def check_settlement(sender, instance, created, **kwargs):
    if created and not settings.USE_PERIODIC_TASK:
        with transaction.atomic():
            not_settled_settlements = ExchangeSettlement.objects.select_for_update().filter(
                state=ExchangeSettlement.STATE_PROCESSING,
                settlement_date__isnull=True
            ).order_by('created_date')

            if not not_settled_settlements.exists():
                not_settled_settlement = ExchangeSettlement.objects.create(
                    state=ExchangeSettlement.STATE_PROCESSING,
                    amount=instance.total_price,
                )
                not_settled_settlement.orders.add(instance)
            else:
                not_settled_settlement = not_settled_settlements.first()
                not_settled_settlement.amount += instance.total_price
                not_settled_settlement.orders.add(instance)

            if not_settled_settlement.amount > 10:
                # call API
                not_settled_settlement.refresh_from_db()
                not_settled_settlement.state = ExchangeSettlement.STATE_DONE
                not_settled_settlement.settlement_date = timezone.now()
                not_settled_settlement.orders.update(is_settled=True)

            not_settled_settlement.save()
