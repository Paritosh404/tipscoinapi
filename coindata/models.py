from django.db import models
import requests
from tipscoin.settings import crypto_api1
from datetime import datetime, timezone
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

    def save(self, *args, **kwargs):
        url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd/inr.json"
        try:
            response = requests.request("GET", url).json()
            cnv_rate = response["inr"]
        except:
            cnv_rate = 0

        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug={}".format(self.slug)

        payload={}
        headers = {
        'X-CMC_PRO_API_KEY': '{}'.format(crypto_api1)
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        for i in response['data']:
            CurrencyData(currency_name=response['data'][i]['name'], currency_symbol=response['data'][i]['symbol'], image_url=self.image_url, slug=response['data'][i]['slug'],rank=response['data'][i]['cmc_rank'], 
                        usd_price=response['data'][i]['quote']['USD']['price'], inr_price=response['data'][i]['quote']['USD']['price']*cnv_rate, volume_24h=response['data'][i]['quote']['USD']['volume_24h'], 
                        percent_change_1h=response['data'][i]['quote']['USD']['percent_change_1h'], percent_change_24h=response['data'][i]['quote']['USD']['percent_change_24h'], percent_change_7d=response['data'][i]['quote']['USD']['percent_change_7d'],
                        percent_change_30d=response['data'][i]['quote']['USD']['percent_change_30d'],percent_change_60d=response['data'][i]['quote']['USD']['percent_change_60d'], percent_change_90d=response['data'][i]['quote']['USD']['percent_change_90d'], 
                        market_cap=response['data'][i]['quote']['USD']['market_cap'], last_updated=response['data'][i]['quote']['USD']['last_updated'], lastcall=datetime.now(timezone.utc)).save()

            CoinUpdate(currency_name=response['data'][i]['name'], current_price=response['data'][i]['quote']['USD']['price'], current_percent_change_1h=response['data'][i]['quote']['USD']['percent_change_1h'],
                        old_5m_percent_change_1h=0,current_percent_change_24h=response['data'][i]['quote']['USD']['percent_change_24h'],old_5m_percent_change_24h=0,old_price_5m=0,old_price_10m=0, change_percenage_5m=0, change_percenage_10m = 0).save()
        super(CoindToGet, self).save( *args, **kwargs)

class ApiCount(models.Model):
    api_name = models.CharField(max_length=30)
    count_check = models.BooleanField(default=False)