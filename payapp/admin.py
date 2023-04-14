from django.contrib import admin
from .models import Notification, NotificationHistory, BalanceHistory, Transaction

admin.site.register(Notification)
admin.site.register(NotificationHistory)
admin.site.register(BalanceHistory)
admin.site.register(Transaction)
