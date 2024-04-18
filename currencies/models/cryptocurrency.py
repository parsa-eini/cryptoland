from django.db import models


class CryptoCurrency(models.Model):
    name = models.SlugField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in USD")

    def __str__(self):
        return f"{self.name} {self.price}$"
