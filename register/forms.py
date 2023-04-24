from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import User, Currency
from django.core.exceptions import ValidationError


# The form used to register the user
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=32, help_text="Required. Enter your last name.")
    email = forms.EmailField(max_length=64, help_text="Required. Enter a valid email address.")
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        to_field_name='currency_type',
        help_text="Select the currency you'd like to use",
        empty_label=None)

    # make sure email is unique
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "currency"]
