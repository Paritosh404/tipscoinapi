from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from .models import CoinSuggestion, UserAlert, UserData
from coindata.models import CoinUpdate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = UserData
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_no': {'write_only': True}
            }
            
    def create(self, validated_data):
        usr = User.objects.create(username=self.validated_data['email'])
        usr.set_password(validated_data['password'])
        usr.save()
        tkn = Token.objects.create(user=usr)
        tkn.save()
        validated_data.pop('password', None)
        user = UserData(**validated_data)
        user.save()
        return user

class UserAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAlert
        fields = "__all__"

    def create(self, validated_data):
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

class CoinSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinSuggestion
        fields = "__all__"