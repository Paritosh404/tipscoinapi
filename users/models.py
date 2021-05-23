from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.

class UserData(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    provider = models.CharField(max_length=25, blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)
    phone_no = models.BigIntegerField(validators=[MaxValueValidator(99999999999), MinValueValidator(0)], null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserAlert(models.Model):
    user_email = models.EmailField()
    coin_name = models.CharField(max_length=25)
    default_alert = models.BooleanField(default=True)
    custom_alert = models.BooleanField(default=False)
    custom_alert_price = models.FloatField(blank=True, null=True)
    custom_alert_percentage = models.FloatField(blank=True, null=True)
    last_send_email = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "UserAlert"
        verbose_name_plural = "User Alerts"
        unique_together = ('user_email', 'coin_name',)

class CoinSuggestion(models.Model):
    user_email = models.EmailField(null=True, blank=True)
    coin_name = models.CharField(max_length=25, unique=True)

    class Meta:
        verbose_name = "Coin Suggestion"
        verbose_name_plural = "Coin Suggestions"
