from django.db import models

from orders.models.order import Order
from utils.models import AbstractTime


class ExchangeSettlement(AbstractTime):
    STATE_DONE = "done"
    STATE_PROCESSING = "processing"
    STATE_CHOICES = (
        (STATE_DONE, "Done"),
        (STATE_PROCESSING, "Processing"),
    )

    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=STATE_PROCESSING)
    orders = models.ManyToManyField(Order, blank=True, related_name="exchange_settlements")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    settlement_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.amount} {self.settlement_date}"