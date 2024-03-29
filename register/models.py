from django.contrib.auth.models import AbstractUser
from django.db import models


# Represents the currencies being used in the app
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


# represents the conversionRates of the currencies
class ConversionRate(models.Model):
    currency_from = models.ForeignKey(Currency, on_delete=models.CASCADE, default=Currency.CurrencyType.POUND,
                                      related_name='from_currency')
    currency_to = models.ForeignKey(Currency, on_delete=models.CASCADE, default=Currency.CurrencyType.POUND,
                                    related_name='to_currency')
    rate = models.DecimalField(decimal_places=3, max_digits=6, default=1)

    def __str__(self):
        return self.currency_from.pk + ' to ' + self.currency_to.pk + ': ' + self.rate.__str__()


#######
# Create custom User Model
# that way we can link preferred currency and balance to user
class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=Currency.CurrencyType.POUND)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=1000)
