from django.db import models

from register.models import User


# Create your models here.
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


# Represents each Transaction who was involved and the amount - only completed transactions here
class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='to_user')
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)


# Represents a History of Balances after transactions for each party involved
class BalanceHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)


# Two types of notification
# = payment into current user's account (to user from another)
# = payment request from current user's account (from user to another)
class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='to_user')
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    dismissed = models.BooleanField()
