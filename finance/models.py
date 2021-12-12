from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.
class transaction(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    symbol = models.CharField(max_length=40)
    company_name = models.CharField(max_length=255)
    needed_money = models.FloatField()
    #type buy or sell
    #konto usera

class userAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique = True)
    money = models.FloatField(default = 0.0)
# pk_522e0372c5f1413c9a271914bddc91ae 

