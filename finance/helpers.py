from django.contrib import messages
import requests
import urllib.parse
import environ
from .models import transaction, userAccount, portfolio
env = environ.Env()
environ.Env.read_env()


def lookup(symbol):
    try:
        api_key = env("API_KEY")
        response = requests.get(
            f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None
# https://cloud.iexapis.com/stable/stock/nflx/quote?token=pk_522e0372c5f1413c9a271914bddc91ae


def updateBuyPaylod(paylod, request, value_to_set):
    for item in value_to_set.items():
        paylod[item[0]] = item[1]
    return paylod


def multiply(a, b):
    a = float(a)
    b = float(b)
    return a * b


def get_user_account(user_id):
    try:
        account = userAccount.objects.get(user=user_id.id)
        return account
    except (userAccount.DoesNotExist):
        raise custom_exception("error no account")

def have_money(needed_money, user_money):
    if needed_money > user_money:
        return False
    else:
        money = user_money - needed_money
        return money
    
def add_message(request, text):
    messages.add_message(request, messages.INFO, text)
    
def get_user_portfolio(request):
    shares = portfolio.objects.filter(buyer=request.user.id)
    return shares      
class custom_exception(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message
