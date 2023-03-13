from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    # ensure user is logged in
    if request.user.is_authenticated:
        ######
        # get all transactions
        ######
        return render(request, 'payapp/home.html')
    else:
        return redirect('login')


def request_payment(request):
    return None


def make_payment(request):
    return None