from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from .models import UserAlert, UserData
from coindata.models import CoinUpdate
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = UserData
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            }
            
    def create(self, validated_data):
        print('here')
        User.objects.create(username=self.validated_data['email'],password=self.validated_data['password'])
        userdata = UserData.objects.create(firstname=self.validated_data['firstname'], lastname=self.validated_data['lastname'], email=self.validated_data['email'], phone_no=self.validated_data['phone_no'], provider=self.validated_data['provider'])
        return userdata

class UserAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAlert
        fields = "__all__"

    def create(self, validated_data):
        print('here')
        coins = CoinUpdate.objects.values('currency_name')
        fnd = False
        for i in coins:
            if i['currency_name'] == self.validated_data['coin_name']:
                fnd = True
                break
        if fnd:
            useralerts = UserAlert.objects.create(user_email=self.validated_data['user_email'], coin_name=self.validated_data['coin_name'])
            return useralerts
        else:
            raise serializers.ValidationError("detail: Coin Does Not exists.")