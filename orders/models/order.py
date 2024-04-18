from django.contrib.auth.models import User
from django.db import models

from currencies.models import CryptoCurrency
from utils.models import AbstractTime


class Order(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_currency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    crypto_currency_price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_date = models.DateTimeField(null=True, blank=True)
    is_settled = models.BooleanField(default=False)

    def __str__(self):
        return f"""
        {self.user} {self.count}
         {self.crypto_currency} at {self.crypto_currency_price} = {self.total_price}
        """
