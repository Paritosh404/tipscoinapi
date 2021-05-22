from django.conf.urls import include, url
from django.db import router
from django.urls import path
from .views import CurrencyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', CurrencyView, basename='currency')

urlpatterns =[
    path('', include(router.urls))
]
