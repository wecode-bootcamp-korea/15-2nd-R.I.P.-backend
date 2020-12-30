from django.db import models

from rip.core import TimeStampModel


class OrderStatus(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'order_status'


class PaymentMethod(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'payment_method'


class OrderDetail(TimeStampModel):
    customer_name    = models.CharField(max_length = 45)
    address          = models.CharField(max_length = 300)
    phone_number     = models.CharField(max_length = 11)
    delivery_message = models.CharField(max_length = 300)

    class Meta:
        db_table = 'order_details'


class Order(TimeStampModel):
    user           = models.ForeignKey("user.User", on_delete = models.PROTECT)
    status         = models.ForeignKey(OrderStatus, on_delete = models.PROTECT)
    detail         = models.ForeignKey(OrderDetail, on_delete = models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete = models.PROTECT)

    class Meta:
        db_table = 'orders'
