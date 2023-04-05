from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from payapp.forms import PayForm
from payapp.models import Notification, BalanceHistory, Transaction, NotificationHistory
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def home(request):
    # ensure user is logged in
    if request.user.is_authenticated:
        if request.GET.get('notification'):
            n = Notification.objects.filter(pk=request.GET.get('notification')).first()
            n.dismissed = True
            n.save()
            return redirect('home')
        if request.GET.get('transaction'):
            n = Transaction.objects.filter(pk=request.GET.get('transaction')).first()
            n.dismissed = True
            n.save()
            return redirect('home')
        ######
        # get all request notifications (from user to another)
        ######
        requests_list = NotificationHistory.objects \
            .filter(notification__from_user=request.user.pk) \
            .filter(dismissed=False)
        print(requests_list)
        ######
        # get all requested notifications (to user from another)
        ######
        payment_request_list = NotificationHistory.objects \
            .filter(notification__to_user=request.user.pk) \
            .filter(dismissed=False)
        print(payment_request_list)
        ######
        # get all transaction notifications
        ######
        transaction_list = BalanceHistory.objects \
            .filter(user=request.user.pk) \
            .filter(dismissed=False)
        print(payment_request_list)
        ######
        # get all transactions relating to user
        ######
        balance_history = BalanceHistory.objects \
            .filter(user=request.user.pk)\
            .order_by('-pk')
        print(balance_history)

        # send to template
        return render(request, 'payapp/home.html', {
            'requests_list': requests_list,
            'payment_request_list': payment_request_list,
            'balance_history': balance_history
        })
    else:
        return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
@transaction.atomic
def payment(request):
    if request.user.is_authenticated:
        form_title = ''
        if request.method == 'POST':
            pay_form = PayForm(request.POST, user=request.user)
            if pay_form.is_valid():
                form_user = pay_form.cleaned_data['form_user']
                form_amount = pay_form.cleaned_data['form_amount']
                # request.path
                # work out if request or send
                # add to respective model
                if request.path == '/request/':
                    # set notification of request (a request)
                    n = Notification(from_user=form_user, to_user=request.user, amount=form_amount, dismissed=False)

                    n.save()
                    return redirect('home')
                elif request.path == '/send/':
                    # set notification that money sent (a payment)
                    # n = Notification(from_user=request.user, to_user=form_user, amount=form_amount, dismissed=False)
                    # n.save()
                    # set money for each party
                    # transaction uses the request.user's currency
                    t = Transaction(from_user=request.user, to_user=form_user, amount=form_amount)
                    t.save()
                    request.user.balance = request.user.balance - form_amount
                    request.user.save()
                    bh_from = BalanceHistory(transaction=t, user=request.user, balance=request.user.balance)
                    bh_from.save()
                    form_user.balance = form_user.balance + form_amount
                    form_user.save()
                    bh_to = BalanceHistory(transaction=t, user=form_user, balance=form_user.balance)
                    bh_to.save()
                    # modify to use RESTful service

                    return redirect('home')
                else:
                    # error - path is not recognised
                    return redirect('home')
            messages.error(request, "Unsuccessful Request. Invalid info")
        else:
            if request.path == '/request/':
                form_title = 'Request Money'
            elif request.path == '/send/':
                form_title = 'Send Money'
            pay_form = PayForm(user=request.user)

        return render(request, 'payapp/payform.html', {'pay_form': pay_form, 'form_title': form_title})
    else:
        return redirect('login')
