from django.shortcuts import render
from requests.sessions import default_headers
from .serializers import CurrencyDataSerializer, CoinToGetSerializer
from users.serailizers import UserAlertSerializer
from .models import ApiCount, CurrencyData, CoindToGet, CoinUpdate
from rest_framework import viewsets, mixins
from users.models import UserAlert, UserData
import requests
import json
from datetime import datetime, timedelta, timezone
from django.core.mail import EmailMultiAlternatives
from tipscoin.settings import crypto_api1, crypto_api2
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
# Create your views here.

mail_from = 'paritoshthakur3655@gmail.com'


    
def render_email(message,mail_to, bcc):
    email = EmailMultiAlternatives('Crypto Coin Market Update', message, mail_from, mail_to, bcc)
    email.send(fail_silently=True)

def percentage_change(current_price, old_price):
    if current_price > old_price:
        chng = ((current_price - old_price) / old_price) * 100
    else:
        chng = ((old_price - current_price) / old_price) * 100
        chng = -abs(chng)
    return chng


def check_change(currency_data, coin_update):
    user_list = []
    alerts = UserAlert.objects.filter(coin_name=currency_data.currency_name, default_alert=True)
    if alerts != []:
        for i in alerts:
            user_list.append(i.user_email)
        change5min = False
        change10min = False
        if (coin_update.change_percenage_5m > 0 and coin_update.change_percenage_5m > 5) or (coin_update.change_percenage_5m < 0 and coin_update.change_percenage_5m < -5):
            market_type = "Up" if coin_update.change_percenage_5m > 0 else "down"
            change5min = "The {0} is {1} by {2} percent in previous 5 mins".format(currency_data.currency_name, market_type, coin_update.change_percenage_5m)
        if (coin_update.change_percenage_10m > 0 and coin_update.change_percenage_10m > 5) or (coin_update.change_percenage_10m < 0 and coin_update.change_percenage_10m < -5):
            market_type = "Up" if coin_update.change_percenage_10m > 0 else "down"
            change10min = "The {0} is {1} by {2} percent in previous 10 mins".format(currency_data.currency_name, market_type, coin_update.change_percenage_10m)
        if change5min and change10min:
            message = change5min + 'and' + change10min
            render_email(message, user_list)
        elif change5min:
            render_email(change5min, user_list)
        elif change10min:
            render_email(change10min, user_list)
    else:
        return False


def get_crypto_update():
    print(datetime.now(), "Update Call Initiated")
    try:
        api = ApiCount.objects.get(api_name='coinmp')
        cnt = api.count_check
    except:
        cnt = True
        api = ApiCount(api_name='coinmp', count_check=cnt).save()
    if cnt:
        api.count_check = False
        api.save()
        key = crypto_api1
    else:
        api.count_check = True
        api.save()
        key = crypto_api2
    coin_names = ''
    coins = CoindToGet.objects.all()
    for i in coins:
        if coin_names == '':
            coin_names = str(i.slug)
        else:
            coin_names = coin_names + ',' + str(i.slug)
    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd/inr.json"
    try:
        response = requests.request("GET", url).json()
        cnv_rate = response["inr"]
    except:
        cnv_rate = 0

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug={}".format(coin_names)

    payload={}
    headers = {
    'X-CMC_PRO_API_KEY': '{}'.format(key)
    }
    response = requests.request("GET", url, headers=headers, data=payload).json()
    for i in response['data']:
        try:
            currency_data = CurrencyData.objects.get(currency_name=response['data'][i]['name'])
            currency_update = CoinUpdate.objects.get(currency_name=response['data'][i]['name'])
        except:
            currency_data = False
            currency_update = False
        if currency_data and currency_update:
            currency_data.rank = response['data'][i]['cmc_rank']
            currency_data.usd_price = response['data'][i]['quote']['USD']['price']
            currency_data.inr_price = response['data'][i]['quote']['USD']['price']*cnv_rate
            currency_data.volume_24h = response['data'][i]['quote']['USD']['volume_24h']
            currency_data.percent_change_1h = response['data'][i]['quote']['USD']['percent_change_1h']
            currency_data.percent_change_24h = response['data'][i]['quote']['USD']['percent_change_24h']
            currency_data.percent_change_7d = response['data'][i]['quote']['USD']['percent_change_7d']
            currency_data.percent_change_30d = response['data'][i]['quote']['USD']['percent_change_30d']
            currency_data.percent_change_60d = response['data'][i]['quote']['USD']['percent_change_60d']
            currency_data.percent_change_90d = response['data'][i]['quote']['USD']['percent_change_90d']
            currency_data.market_cap = response['data'][i]['quote']['USD']['market_cap']
            currency_data.last_updated = response['data'][i]['quote']['USD']['last_updated']
            currency_data.lastcall = datetime.now(timezone.utc)
            currency_data.save()

            currency_update = CoinUpdate.objects.get(currency_name=response['data'][i]['name'])
            currency_update.old_5m_percent_change_24h = currency_update.current_percent_change_24h
            currency_update.old_price_5m = currency_update.current_price
            currency_update.old_price_10m = currency_update.old_price_5m
            currency_update.old_5m_percent_change_1h = currency_update.current_percent_change_1h
            currency_update.current_price = response['data'][i]['quote']['USD']['price']
            currency_update.current_percent_change_1h = response['data'][i]['quote']['USD']['percent_change_1h']
            currency_update.current_percent_change_24h = response['data'][i]['quote']['USD']['percent_change_24h']
            currency_update.save()
            currency_update.change_percenage_5m = float(percentage_change(currency_update.current_price, currency_update.old_price_5m))
            currency_update.change_percenage_10m = float(percentage_change(currency_update.current_price, currency_update.old_price_10m))
            currency_update.save()
        else:
            CoindToGet.objects.get(slug=response['data'][i]['slug']).image_url
            CurrencyData(currency_name=response['data'][i]['name'], currency_symbol=response['data'][i]['symbol'], image_url=CoindToGet.objects.get(slug=response['data'][i]['slug']).image_url, slug=response['data'][i]['slug'],rank=response['data'][i]['cmc_rank'], 
                        usd_price=response['data'][i]['quote']['USD']['price'], inr_price=response['data'][i]['quote']['USD']['price']*cnv_rate, volume_24h=response['data'][i]['quote']['USD']['volume_24h'], 
                        percent_change_1h=response['data'][i]['quote']['USD']['percent_change_1h'], percent_change_24h=response['data'][i]['quote']['USD']['percent_change_24h'], percent_change_7d=response['data'][i]['quote']['USD']['percent_change_7d'],
                        percent_change_30d=response['data'][i]['quote']['USD']['percent_change_30d'],percent_change_60d=response['data'][i]['quote']['USD']['percent_change_60d'], percent_change_90d=response['data'][i]['quote']['USD']['percent_change_90d'], 
                        market_cap=response['data'][i]['quote']['USD']['market_cap'], last_updated=response['data'][i]['quote']['USD']['last_updated'], lastcall=datetime.now(timezone.utc)).save()

            CoinUpdate(currency_name=response['data'][i]['name'], current_price=response['data'][i]['quote']['USD']['price'], current_percent_change_1h=response['data'][i]['quote']['USD']['percent_change_1h'],
                        old_5m_percent_change_1h=0,current_percent_change_24h=response['data'][i]['quote']['USD']['percent_change_24h'],old_5m_percent_change_24h=0,old_price_5m=0,old_price_10m=0, change_percenage_5m=0, change_percenage_10m = 0).save()

def alert_check():
    change_delta5m = 0
    change_delta10m = 0
    change5min = False
    change10min = False
    message = False
    users = UserData.objects.all()
    for i in users:
        alerts = UserAlert.objects.filter(user_email=str(i.email))
        for j in alerts:
            coin_update = CoinUpdate.objects.get(currency_name=j.coin_name)
            if (coin_update.change_percenage_5m > 0 and coin_update.change_percenage_5m > 2) or (coin_update.change_percenage_5m < 0 and coin_update.change_percenage_5m < -2):
                change_delta5m = coin_update.change_percenage_5m
                market_type = "Up" if coin_update.change_percenage_5m > 0 else "down"
                change5min = "The {0} is {1} by {2} percent in previous 5 mins.\n".format(j.coin_name, market_type, coin_update.change_percenage_5m)
            if (coin_update.change_percenage_10m > 0 and coin_update.change_percenage_10m > 2) or (coin_update.change_percenage_10m < 0 and coin_update.change_percenage_10m < -2):
                change_delta10m = coin_update.change_percenage_5m
                market_type = "Up" if coin_update.change_percenage_10m > 0 else "down"
                change10min = "The {0} is {1} by {2} percent in previous 10 min.\n".format(j.coin_name, market_type, coin_update.change_percenage_10m)
            if change5min and change10min:
                message = change5min + change10min if message == False else message + change5min + change10min
            elif change5min:
                message = change5min if message == False else message + change5min
            elif change10min:
                message = change10min if message == False else message + change10min
        if j.last_send_email == None and message:
            render_email(message, list(str(i.email)), [])
        elif j.last_send_email < (datetime.now(timezone.utc) + timedelta(minutes = 15)) and message:
            render_email(message, list(str(i.email)), [])
        elif (change_delta5m > 10 and message) or (change_delta10m > 10 and message):
            render_email(message, list(str(i.email)), [])
        elif (change_delta5m < -10 and message) or (change_delta10m <-10 and message):
            render_email(message, list(str(i.email)), [])

scheduler = BackgroundScheduler()
scheduler.add_job(get_crypto_update, "interval", seconds=150, id='currency001', replace_existing=True)
scheduler.start()
#get_crypto_update()

class CurrencyView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = CurrencyData.objects.all().order_by('rank')
    serializer_class = CurrencyDataSerializer
    lookup_field = "currency_name"
    lookup_value_regex = "[^/]+"


