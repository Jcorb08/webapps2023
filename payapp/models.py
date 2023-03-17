from django.db import models

from register.models import User


# Create your models here.
class Currency(models.Model):
    class CurrencyType(models.TextChoices):
        DOLLAR = 'USD'
        POUND = 'GBP'
        EURO = 'EUR'

    currency_type = models.CharField(
        max_length=3,
        choices=CurrencyType.choices,
        default=CurrencyType.POUND,
        primary_key=True)

    class CurrencySymbol(models.TextChoices):
        DOLLAR = '$'
        POUND = '£'
        EURO = '€'

    symbol = models.CharField(
        max_length=1,
        choices=CurrencySymbol.choices,
        default=CurrencySymbol.POUND)

    def __str__(self):
        return self.currency_type + ' ' + self.symbol


class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='to_user')
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    # how to keep track of balance after transactions


class Notification(models.Model):
    pass
