from rest_framework.views import APIView
from rest_framework import permissions  # , authentication
from rest_framework.response import Response

from api.exception import CurrencyIncorrect
from register.models import Currency, ConversionRate


# Create your views here.
class Conversion(APIView):
    # requires a tokenAuth and only Users can access this view
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
            amount = self.kwargs['amount'] * conversion_rate.rate
            response['amount'] = amount
        except KeyError:
            pass
        return Response(response)
