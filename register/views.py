from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from finance.models import userAccount
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            userAccount.objects.create(user=new_user, money=10000.00)
        else:
           messages.add_message(request, messages.INFO, form.errors)    
        return redirect("/")        
    else:    
        form = UserCreationForm()
    return render(request, "register/register.html", {"form": form});
