from django.db import models
from django.db.models.query import QuerySet
from django.db.utils import DataError, Error
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import UserAlert, UserData
from coindata.models import CoinUpdate
from rest_framework import generics
from rest_framework import mixins, viewsets
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from .serailizers import UserAlertSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg import openapi
# Create your views here.

coin_name = openapi.Parameter('coin_name', in_=openapi.IN_QUERY, description='coin_name',
                                type=openapi.TYPE_STRING)

user_alert_response = openapi.Response('response description', UserAlertSerializer)


class UserViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = UserData.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = "email"
    lookup_value_regex = "[^/]+" 
    

class UserAlertViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, 
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = UserAlert.objects.all().order_by('id')
    serializer_class = UserAlertSerializer
    lookup_field = "user_email"
    lookup_value_regex = "[^/]+"

    @swagger_auto_schema(
        manual_parameters=[coin_name],
        responses={
            200: UserAlertSerializer,
            400: "Bad Request",
        },
        
    )

    def retrieve(self, request, user_email):
        try:
            coin = request.GET['coin_name']
        except:
            coin = False
        if coin:
            alerts = UserAlert.objects.filter(user_email=user_email, coin_name=coin )
        else:
            alerts = UserAlert.objects.filter(user_email=user_email)
        data = UserAlertSerializer(alerts, many=True).data
        if data == []:
            return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data)

    @swagger_auto_schema(
        manual_parameters=[coin_name],
    )

    def destroy(self, request, user_email):
        data={}
        try:
            coin = request.GET['coin_name']
        except:
            return Response({"detail": "Coin Name Required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            alerts = UserAlert.objects.get(user_email=user_email, coin_name=coin)
        except UserAlert.DoesNotExist:
            data["detail"] = "Alert Not found."
            return Response(data, status= status.HTTP_404_NOT_FOUND)
        operation = alerts.delete()    
        if operation:
            data["detail"]= "successful"
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data["detail"] = "failure"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from django.template import RequestContext

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response



