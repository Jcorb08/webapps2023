from enum import unique

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from payapp.models import Currency


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=32, help_text="Required. Enter your last name.")
    email = forms.EmailField(max_length=64, help_text="Required. Enter a valid email address.")
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        help_text="Select the currency you'd like to use",
        empty_label=None)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "currency"]
