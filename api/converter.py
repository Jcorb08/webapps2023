from decimal import Decimal
from django.core.exceptions import ValidationError


class DecimalConverter:
    # matches a whole number or a number with up to two decimal points
    regex = r'\d+(?:\.\d{1,2})?'

    def to_python(self, value):
        try:
            return Decimal(value)
        except ValueError:
            raise ValidationError('Enter a valid decimal number.')

    def to_url(self, value):
        return str(value)
