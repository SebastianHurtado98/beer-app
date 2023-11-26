from django.db import models
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    name = models.CharField(max_length=100)

class Beer(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    name = models.CharField(max_length=100)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    billed = models.BooleanField(default=False)

class PaymentType(models.TextChoices):
    INDIVIDUAL = 'IND', _('Individual')
    GROUP = 'GRP', _('Group')

class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_type = models.CharField(
        max_length=3,
        choices=PaymentType.choices,
        default=PaymentType.INDIVIDUAL,
    )
