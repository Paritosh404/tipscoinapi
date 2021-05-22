from django.conf.urls import include, url
from django.db import router
from django.urls import path
from .views import UserAlertViewSet, UserViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register(r'account', UserViewSet, basename='users')
router.register(r'setalert', UserAlertViewSet, basename='setalert')

urlpatterns =[
    path('', include(router.urls)),
]
