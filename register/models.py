from django.contrib.auth.models import AbstractUser
from django.db import models
from payapp.models import Currency


#######
# Create custom User Model
# that way we can link preferred currency and balance to user
class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, default=Currency.CurrencyType.POUND)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
