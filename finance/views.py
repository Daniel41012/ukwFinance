from multiprocessing import context
from django.shortcuts import render
from .models import transaction, userAccount, portfolio
from rest_framework import generics
from .serializer import transactionSerializer, userAccountSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .helpers import lookup, updateBuyPaylod, multiply, get_user_account, have_money, add_message, get_user_portfolio

# Create your views here.


def index(request):
    return render(request, "finance/base.html", {})


def buy(request):
    return render(request, "finance/buy.html", {})





@api_view(['GET', 'POST'])
def transactionListView(request):
    if request.method == "GET":
        transactions = transaction.objects.all()
        serializer = transactionSerializer(transactions, many=True)
        return Response(serializer.data)

    elif request.method == "POST":

        request.POST._mutable = True
        symbol = request.POST["symbol"]

        if not symbol:
            add_message(request, "No symbol")
            return render(request, "finance/base.html", {})

        symbol = symbol.upper()
        values = lookup(symbol)
        quantity = request.POST.get("quantity")
        
        if not quantity:
            add_message(request, "Shares can't be 0")
            return render(request, "finance/base.html", {})

        final_amount = multiply(quantity, values.get("price"))
        user_account = get_user_account(request.user)
        user_money = user_account.money
        account_balance = have_money(final_amount, user_money)

        if int(quantity) <= 0:
            add_message(request, "Shares can't be 0")
            return render(request, "finance/base.html", {})

        if not account_balance:
            add_message(request, 'Not enough founds')
            return render(request, "finance/base.html", {})

        obj = {'company_name': values.get('name'),
               'buyer': request.user.id,
               'transaction_type': 1,
               'needed_money': round(final_amount,2),
               'price': values.get('price'),
               'user_account': user_account.id,
               'symbol': symbol
               }

        updateBuyPaylod(request.POST, request, obj)

        serializer = transactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_account.money = round(account_balance, 2)
            user_account.save()
            portfolios = portfolio.objects.filter(buyer=request.user.id)
            portfolios = portfolios.filter(symbol=symbol)

            if portfolios:
                for port in portfolios:
                    port.quantity += int(quantity)
                    port.save()
            else:
                port = portfolio(buyer=request.user,
                                 symbol=symbol, quantity=quantity)
                port.save()
            add_message(request, 'Hooray! purchase completed')
            return render(request, "finance/base.html", {})

        add_message(request, 'Something went wrong ' + serializer.errors)
        return render(request, "finance/base.html", {})


@api_view(['GET', 'POST'])
def quote(request):
    data = {}
    if request.method == "POST":

        symbol = request.POST["symbol"]
        if not symbol:
            add_message(request, "No symbol")
            return render(request, "finance/base.html", {})

        data = lookup(symbol)
    return render(request, "finance/quote.html", {"data": data})


@api_view(['GET', 'POST'])
def sell(request):
    if request.method == "POST":
        request.POST._mutable = True
        symbols = portfolio.objects.filter(buyer=request.user.id)
        symbols = symbols.filter(symbol=request.POST["symbol"].upper())
        shares = request.POST["shares"]
        values = lookup(request.POST["symbol"])
        final_amount = multiply(shares, values.get("price"))
        user_account = get_user_account(request.user)
        
        for s in symbols:
            if s.quantity < int(shares):
                
                add_message(request, "Not enough shares ")
                symbols = portfolio.objects.filter(buyer=request.user.id)
                return render(request, "finance/sell.html", {"symbols": symbols})
            
            elif s.quantity > int(shares):
                
                s.quantity -= int(shares)
                s.save()
                
            else:
                s.delete()
            obj = {'company_name': values.get('name'),
                    'buyer': request.user.id,
                    'transaction_type': 0,
                    'needed_money': final_amount,
                    'quantity': shares,
                    'price': values.get('price'),
                    'user_account': user_account.id
                    }

            updateBuyPaylod(request.POST, request, obj)
            serializer = transactionSerializer(data=request.data)
            
            
            if serializer.is_valid():
                serializer.save()
            add_message(request, "Shares sold")
            symbols = portfolio.objects.filter(buyer=request.user.id)
            
        return render(request, "finance/sell.html", {"symbols": symbols})
    else:
        symbols = get_user_portfolio(request)
        return render(request, "finance/sell.html", {"symbols": symbols})

def history(request):
    stocks =transaction.objects.filter(buyer=request.user.id).order_by('-created_at')
        
        
    return render(request, "finance/history.html", {"stocks":stocks})

class transactionDetailView (generics.RetrieveUpdateDestroyAPIView):
    queryset = transaction.objects.all()
    serializer_class = transactionSerializer


class userAccountListView(generics.ListCreateAPIView):
    queryset = userAccount.objects.all()
    serializer_class = userAccountSerializer


class userAccountDetailView (generics.RetrieveUpdateAPIView):
    queryset = userAccount.objects.all()
    serializer_class = userAccountSerializer
