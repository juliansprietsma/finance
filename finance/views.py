from django.shortcuts import render, redirect

from .models import TransactionCategory, Transaction

# Create your views here.
def home(request):
    if request.user.is_authenticated:

        print("ID: ", request.user.id)

        user_categories = TransactionCategory.objects.filter(user__id=request.user.id)

        user_transactions = Transaction.objects.filter(user__id=request.user.id)

        context = {
            'categories': user_categories,
            'transactions': user_transactions,
        }

        return render(request, "finance/home.html", context)
    else:
        return redirect('accounts/login')

def profile(request):
    pass

