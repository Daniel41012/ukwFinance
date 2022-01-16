from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.


class userAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique = True, related_name = "owner")
    money = models.FloatField(default = 0.0)
# pk_522e0372c5f1413c9a271914bddc91ae
#https://cloud.iexapis.com/stable/stock/nflx/quote?token=pk_522e0372c5f1413c9a271914bddc91ae 


class transaction(models.Model):
    transaction_choice = [("0","Sell"),("1","Buy")]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    symbol = models.CharField(max_length=40)
    company_name = models.CharField(max_length=255)
    needed_money = models.FloatField()
    transaction_type = models.CharField(max_length=40, choices=transaction_choice)
    user_account = models.ForeignKey(userAccount,on_delete=models.CASCADE,related_name = "account")
    created_at = models.DateTimeField(auto_now_add=True)
    
class portfolio(models.Model):    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=40)
    quantity = models.IntegerField()

