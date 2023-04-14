from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterForm
from .models import User, Currency, ConversionRate


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display.__add__(('currency', 'balance'))
    add_form = RegisterForm
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('currency', 'balance')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Currency)
admin.site.register(ConversionRate)
