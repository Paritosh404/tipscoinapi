from django.db.models import fields
from .models import CoindToGet, CurrencyData
from rest_framework import serializers


class CurrencyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyData
        fields = "__all__"

class CoinToGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoindToGet
        fields = '__all__'