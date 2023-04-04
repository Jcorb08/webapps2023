from django.shortcuts import render, redirect
from django.contrib import messages
from payapp.forms import PayForm
from payapp.models import Notification, BalanceHistory


def home(request):
    # ensure user is logged in
    if request.user.is_authenticated:
        if request.GET.get('notification'):
            n = Notification.objects.filter(pk=request.GET.get('notification')).first()
            n.dismissed = True
            n.save()
            return redirect('home')

        ######
        # get all request notifications (from user to another)
        ######
        requests_list = Notification.objects\
            .filter(from_user=request.user.pk)\
            .filter(dismissed=False)
        print(requests_list)
        ######
        # get all payment notifications (to user from another)
        ######
        requested_list = Notification.objects\
            .filter(to_user=request.user.pk)\
            .filter(dismissed=False)
        print(requested_list)
        ######
        # get all transactions relating to user
        ######
        balance_history = BalanceHistory.objects\
            .filter(user=request.user.pk)
        print(balance_history)

        # send to template
        return render(request, 'payapp/home.html', {
            'requests_list': requests_list,
            'requested_list': requested_list,
            'balance_history': balance_history
            })
    else:
        return redirect('login')


def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pay_form = PayForm(request.POST, user=request.user)
            if pay_form.is_valid():
                form_user = pay_form.cleaned_data['form_user']
                form_amount = pay_form.cleaned_data['form_amount']
                # request.path
                # work out if request or send
                # add to respective model
                n = None
                if request.path == '/request/':
                    n = Notification(from_user=form_user, to_user=request.user, amount=form_amount, dismissed=False)
                elif request.path == '/send/':
                    n = Notification(from_user=request.user, to_user=form_user, amount=form_amount, dismissed=False)

                n.save()
                # process at later date-

                # edit render to show field changes on frontend
                return redirect('home')
            messages.error(request, "Unsuccessful Request. Invalid info")
        else:
            pay_form = PayForm(user=request.user)

        return render(request, 'payapp/payform.html', {'pay_form': pay_form})
    else:
        return redirect('login')
