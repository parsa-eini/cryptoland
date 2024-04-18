from django.urls import path

from . import views

app_name = "Payment"

urlpatterns = [
    path("orderpay/", views.OrderPayAPIView.as_view(), name="order_pay"),
]
