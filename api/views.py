from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from api.exception import CurrencyIncorrect
from register.models import Currency, ConversionRate


# Create your views here.
class Conversion(APIView):

    def get(self, request, format=None, **kwargs):
        """
        Return the converted currency
        """
        response = {}
        try:
            currency_from = Currency.objects.get(pk=self.kwargs['currency_from'])
            currency_to = Currency.objects.get(pk=self.kwargs['currency_to'])
        except Currency.DoesNotExist:
            raise CurrencyIncorrect
        conversion_rate = ConversionRate.objects.filter(currency_from=currency_from) \
            .filter(currency_to=currency_to).first()

        response['rate'] = conversion_rate.rate
        try:
            amount = Decimal(self.kwargs['amount']) * Decimal(conversion_rate.rate)
            response['amount'] = round(amount, 2)
        except KeyError:
            pass
        return Response(response)
