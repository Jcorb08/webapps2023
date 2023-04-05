from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from payapp.forms import PayForm
from payapp.models import Notification, BalanceHistory, Transaction, NotificationHistory
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# the home page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def home(request):
    # ensure user is logged in
    if request.user.is_authenticated:
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
            ######
            # get all request notifications (from user to another)
            ######
            requests_list = NotificationHistory.objects \
                .filter(user=request.user.pk)\
                .filter(notification__from_user=request.user.pk) \
                .filter(dismissed=False)
            print(requests_list)
            ######
            # get all requested notifications (to user from another)
            ######
            payment_request_list = NotificationHistory.objects \
                .filter(user=request.user.pk) \
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
                .filter(user=request.user.pk) \
                .order_by('-pk')
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
                        t = Transaction(from_user=request.user, to_user=form_user, amount=form_amount)
                        t.save()
                        request.user.balance = request.user.balance - form_amount
                        request.user.save()
                        bh_from = BalanceHistory(transaction=t, user=request.user,
                                                 balance=request.user.balance, dismissed=False)
                        bh_from.save()
                        form_user.balance = form_user.balance + form_amount
                        form_user.save()
                        bh_to = BalanceHistory(transaction=t, user=form_user, balance=form_user.balance, dismissed=False)
                        bh_to.save()
                        # modify to use RESTful service

                        return redirect('home')
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

