from django.contrib import admin

from orders.models.order import Order


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "crypto_currency",
        "crypto_currency_price",
        "count",
        "total_price",
        "paid_date",
        "is_settled",
    ]
