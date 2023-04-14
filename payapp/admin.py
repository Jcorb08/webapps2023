from django.contrib import admin
from .models import Notification, NotificationHistory, BalanceHistory, Transaction


class NotificationTransactionAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'amount']


class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ['notification', 'user', 'dismissed']


class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'user', 'dismissed','balance']


admin.site.register(Notification, NotificationTransactionAdmin)
admin.site.register(NotificationHistory, NotificationHistoryAdmin)
admin.site.register(BalanceHistory, BalanceHistoryAdmin)
admin.site.register(Transaction, NotificationTransactionAdmin)
