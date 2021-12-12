from django.db import models
from django.db.models import fields
from .models import transaction, userAccount
from rest_framework import serializers


class transactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = transaction
        fields = ['buyer', 'price', 'quantity', 'symbol', 'company_name', 'needed_money']
        
class userAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        
        model = userAccount
        fields = ['user','money']