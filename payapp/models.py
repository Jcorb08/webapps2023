from django.db import models

from register.models import User


# Create your models here.
# Represents each Transaction who was involved and the amount - only completed transactions here
class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_to_user')
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)


# Represents a History of Balances after transactions for each party involved
class BalanceHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dismissed = models.BooleanField(default=False)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)


# Two types of notification
# = request payment sent to another user's account (to user from another)
# = payment request from current user's account (from user to another)
class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to_user')
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)


# Keeps track of which users have dismissed the notification
class NotificationHistory(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dismissed = models.BooleanField(default=False)
