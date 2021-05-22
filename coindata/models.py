from django.db import models

# Create your models here.

class CurrencyData(models.Model):
    currency_name = models.CharField(max_length=30, unique=True)
    currency_symbol = models.CharField(max_length=30)
    image_url = models.CharField(max_length=100)
    slug = models.CharField(max_length=30)
    rank = models.IntegerField()
    usd_price = models.FloatField()
    inr_price = models.FloatField()
    volume_24h = models.FloatField()
    percent_change_1h = models.FloatField()
    percent_change_24h = models.FloatField()
    percent_change_7d = models.FloatField()
    percent_change_30d = models.FloatField()
    percent_change_60d = models.FloatField()
    percent_change_90d =  models.FloatField()
    market_cap = models.FloatField()
    last_updated = models.DateTimeField()
    lastcall = models.DateTimeField()

    class Meta:
        verbose_name = "Currency Data"
        verbose_name_plural = "Currency Data"


class CoinUpdate(models.Model):
    currency_name = models.CharField(max_length=30, unique=True)
    current_price = models.FloatField()
    current_percent_change_1h = models.FloatField()
    old_5m_percent_change_1h = models.FloatField()
    current_percent_change_24h = models.FloatField()
    old_5m_percent_change_24h = models.FloatField()
    old_price_5m = models.FloatField()
    old_price_10m = models.FloatField()
    change_percenage_5m = models.FloatField()
    change_percenage_10m = models.FloatField()

    class Meta:
        verbose_name = "Coin Update"
        verbose_name_plural = "Coin Updates"

class CoindToGet(models.Model):
    slug = models.CharField(max_length=30)
    image_url = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Coin To Get"
        verbose_name_plural = "Coins To Get"

class ApiCount(models.Model):
    api_name = models.CharField(max_length=30)
    count_check = models.BooleanField(default=False)