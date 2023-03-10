from django.db import models


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
