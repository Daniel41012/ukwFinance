from django.db.models import query
from django.shortcuts import render
from .models import transaction, userAccount
from rest_framework import generics
from .serializer import transactionSerializer, userAccountSerializer, UserSerializer
# Create your views here.


class transactionListView (generics.ListCreateAPIView):
    queryset = transaction.objects.all()
    serializer_class = transactionSerializer

class transactionDetailView (generics.RetrieveUpdateDestroyAPIView):
    queryset = transaction.objects.all()
    serializer_class = transactionSerializer


class userAccountListView(generics.ListCreateAPIView):
    queryset = userAccount.objects.all()
    serializer_class = userAccountSerializer


class userAccountDetailView (generics.RetrieveUpdateDestroyAPIView):
    queryset = userAccount.objects.all()
    serializer_class = userAccountSerializer