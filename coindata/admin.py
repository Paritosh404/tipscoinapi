from django.contrib import admin
from .models import ApiCount, CurrencyData, CoinUpdate, CoindToGet
# Register your models here.

class CurrencyDataAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'currency_symbol', 'slug', 'rank', 'usd_price', 'inr_price', 'percent_change_1h', 'percent_change_24h')
    search_fields = ('currency_name', 'currency_symbol')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CoinUpdateAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'current_price')
    search_fields = ('currency_name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CoinToGetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'image_url')
    search_fields = ('slug',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CurrencyData, CurrencyDataAdmin)
admin.site.register(CoinUpdate, CoinUpdateAdmin)
admin.site.register(CoindToGet, CoinToGetAdmin)
admin.site.register(ApiCount)
