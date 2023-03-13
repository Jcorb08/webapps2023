from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            #####
            # use restful service to
            # initialise £1000 in their currency
            # then link to user in balance table
            #####
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid info")
    else:
        register_form = RegisterForm()

    return render(request, 'register/register.html', {'register_user': register_form})


def login_user(request):
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


def logout_user(request):
    logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('login')
