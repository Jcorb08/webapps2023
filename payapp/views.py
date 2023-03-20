from django.shortcuts import render, redirect
from django.contrib import messages

from payapp.forms import PayForm


# Create your views here.
def home(request):
    # ensure user is logged in
    if request.user.is_authenticated:
        ######
        # get all request notifications (from user to another)
        ######
        # get all payment notifications (to user from another)
        ######
        # get all transactions relating to user
        ######
        return render(request, 'payapp/home.html')
    else:
        return redirect('login')


def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pay_form = PayForm(request.POST)
            if pay_form.is_valid():
                # request.path
                # work out if request or send
                # add to respective model for now
                # process at later date

                # edit render to show field changes on frontend
                return redirect('home')
            messages.error(request, "Unsuccessful Request. Invalid info")
        else:
            pay_form = PayForm()

        return render(request, 'payapp/payform.html', {'register_user': pay_form})
    else:
        return redirect('login')

