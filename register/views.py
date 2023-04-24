# Create your views here.
import urllib3
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import requests
from decimal import Decimal


# Create your views here.
@csrf_protect
# register the user
def register_user(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            # initialised £1000
            # use restful service to change to be exchange rate of 1000

            # remove warnings in console due to Unverified HTTPS
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url = 'https://' + request.get_host()
            url += '/conversion/{currency_from}/{currency_to}/{amount}'.format(
                currency_from='GBP',
                currency_to=user.currency.pk,
                amount=Decimal(user.balance)
            )
            # has to be verify False due to SSL certificate being self-signed
            resp = requests.get(url, verify=False).json()
            print(resp)
            # set user balance to converted amount
            user.balance = resp['amount']
            user.save()
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid info")
    else:
        register_form = RegisterForm()

    return render(request, 'register/register.html', {'register_user': register_form})


@csrf_protect
def login_user(request):
    # when login required redirects here remove next querystring
    if request.GET.get('next'):
        return redirect('login')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data.get('username'),
                                password=login_form.cleaned_data.get('password'))
            if user is not None:
                # authenticated
                login(request, user)
                messages.info(request, f"You are now logged in")
                return redirect('home')
            else:
                messages.error(request, 'invalid username/password')
        else:
            messages.error(request, 'invalid username/password')
    else:
        login_form = AuthenticationForm()

    return render(request, 'register/login.html', {'login_user': login_form})


# log user out
def logout_user(request):
    logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('login')
