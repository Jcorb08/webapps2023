from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Currency, ConversionRate

admin.site.register(User, UserAdmin)
admin.site.register(Currency)
admin.site.register(ConversionRate)
