from django.db import models
from django.db.models import fields
from .models import transaction, userAccount,User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username']


        
class userAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=False,read_only=True)
    class Meta:
        model = userAccount
        fields = ['user','money', "users"]
       
class transactionSerializer(serializers.ModelSerializer):
    buyers = UserSerializer(many=False,read_only=True)
    user_accounts = userAccountSerializer(many=False,read_only=True)
    

    class Meta: 
        model = transaction
        fields = ['buyer', 'price', 'quantity', 'symbol', 'company_name', 'needed_money', 'buyers', "transaction_type", "user_accounts", 'user_account']        