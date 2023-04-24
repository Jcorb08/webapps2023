import requests
import urllib3
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from payapp.forms import PayForm
from payapp.models import Notification, BalanceHistory, Transaction, NotificationHistory
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from decimal import Decimal


# the home page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def home(request):
    # ensure user is logged in
    if request.user.is_authenticated:
        # dismiss notifications at the top if removed clicked
        if request.GET.get('notification'):
            n = NotificationHistory.objects.filter(pk=request.GET.get('notification')).first()
            n.dismissed = True
            n.save()
            return redirect('home')
        elif request.GET.get('transaction'):
            n = BalanceHistory.objects.filter(pk=request.GET.get('transaction')).first()
            n.dismissed = True
            n.save()
            return redirect('home')
        else:
            def add_converted_amounts(object_list, linked_table):
                # remove warnings in console due to Unverified HTTPS
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                for single_object in object_list:
                    url = 'https://' + request.get_host()
                    url += '/conversion/{currency_from}/{currency_to}/{amount}'.format(
                        currency_from=getattr(single_object, linked_table).from_user.currency.pk,
                        currency_to=getattr(single_object, linked_table).to_user.currency.pk,
                        amount=Decimal(getattr(single_object, linked_table).amount)
                    )
                    # has to be verify False due to SSL certificate being self-signed
                    resp = requests.get(url, verify=False).json()
                    single_object.converted_amount = round(Decimal(resp['amount']), 2)
                    single_object.rate = resp['rate']
                return object_list

            ######
            # get all request notifications (from user to another)
            # needs conversion
            ######
            requests_list = NotificationHistory.objects \
                .filter(user=request.user.pk)\
                .filter(notification__from_user=request.user.pk) \
                .filter(dismissed=False)

            requests_list = add_converted_amounts(requests_list, 'notification')
            print(requests_list)
            ######
            # get all requested notifications (to user from another)
            # always in user's currency
            ######
            payment_request_list = NotificationHistory.objects \
                .filter(user=request.user.pk) \
                .filter(notification__to_user=request.user.pk) \
                .filter(dismissed=False)
            print(payment_request_list)
            ######
            # get all transaction notifications
            # amount needs conversion
            ######
            transaction_list = BalanceHistory.objects \
                .filter(user=request.user.pk) \
                .filter(dismissed=False)
            transaction_list = add_converted_amounts(transaction_list, 'transaction')
            print(transaction_list)
            ######
            # get all transactions relating to user
            # amount needs conversion
            ######
            balance_history = BalanceHistory.objects \
                .filter(user=request.user.pk) \
                .order_by('-pk')
            balance_history = add_converted_amounts(balance_history, 'transaction')
            print(balance_history)
            # send to template
            return render(request, 'payapp/home.html', {
                'requests_list': requests_list,
                'payment_request_list': payment_request_list,
                'transaction_list': transaction_list,
                'balance_history': balance_history
            })
    else:
        return redirect('login')


# manages the payment form both requests and sending
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
                    n = Notification(from_user=form_user, to_user=request.user, amount=form_amount)
                    n.save()
                    nh_from = NotificationHistory(notification=n, user=form_user, dismissed=False)
                    nh_from.save()
                    nh_to = NotificationHistory(notification=n, user=request.user, dismissed=False)
                    nh_to.save()
                    return redirect('home')
                elif request.path == '/send/':
                    # check there are enough funds!
                    if request.user.balance - form_amount >= 0:
                        # set notification that money sent (a payment)
                        # transaction uses the request.user's currency - need to convert this if form_user different
                        try:
                            # remove warnings in console due to Unverified HTTPS
                            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                            url = 'https://' + request.get_host()
                            t = Transaction(from_user=request.user, to_user=form_user, amount=form_amount)
                            t.save()

                            request.user.balance = request.user.balance - form_amount
                            request.user.save()
                            bh_from = BalanceHistory(transaction=t, user=request.user,
                                                     balance=request.user.balance, dismissed=False)
                            bh_from.save()
                            url += '/conversion/{currency_from}/{currency_to}/{amount}'.format(
                                currency_from=request.user.currency.pk,
                                currency_to=form_user.currency.pk,
                                amount=Decimal(form_amount)
                            )
                            # has to be verify False due to SSL certificate being self-signed
                            resp = requests.get(url, verify=False).json()

                            form_user.balance = Decimal(form_user.balance) + Decimal(resp['amount'])
                            form_user.save()
                            bh_to = BalanceHistory(transaction=t, user=form_user, balance=form_user.balance, dismissed=False)
                            bh_to.save()
                            return redirect('home')
                        except requests.exceptions.JSONDecodeError:
                            messages.error(request, "Unsuccessful Request. Internal Error")
                    else:
                        messages.error(request, "Unsuccessful Request. Insufficient funds")
                else:
                    # error - path is not recognised
                    return redirect('home')
            else:
                messages.error(request, "Unsuccessful Request. Invalid info")

        pay_form = PayForm(user=request.user)
        if request.path == '/request/':
            form_title = 'Request Money'
            pay_form.fields['form_user'].label = 'Request Money from User'
            pay_form.fields['form_amount'].label = 'Amount to Request'
        elif request.path == '/send/':
            pay_form.fields['form_user'].label = 'Send Money to User'
            pay_form.fields['form_amount'].label = 'Amount to Send'
            form_title = 'Send Money'
        return render(request, 'payapp/payform.html', {'pay_form': pay_form, 'form_title': form_title})
    else:
        return redirect('login')

