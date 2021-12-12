from django.contrib import admin
from .models import transaction, userAccount
# Register your models here.





@admin.register(transaction)
class transactionAdmin(admin.ModelAdmin):
    search_fields = ['symbol']
    list_display = ['id', 'buyer', 'symbol', 'quantity']
    list_filter = ['symbol']


@admin.register(userAccount)
class userAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

