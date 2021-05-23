from users.models import CoinSuggestion
from django.conf.urls import include, url
from django.db import router
from django.urls import path
from .views import SuggestionViewSet, UserAlertViewSet, UserViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register(r'account', UserViewSet, basename='users')
router.register(r'setalert', UserAlertViewSet, basename='setalert')
router.register(r'suggestions', SuggestionViewSet, basename='suggestion')

urlpatterns =[
    path('', include(router.urls)),
]
