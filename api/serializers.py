from rest_framework import serializers
from register.models import Currency, ConversionRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ConversionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRate
        fields = '__all__'
