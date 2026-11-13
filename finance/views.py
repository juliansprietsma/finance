from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

from allauth.account.views import EmailView

from django.core.mail import send_mail

from .models import TransactionCategory, Transaction

# Create your views here.
@login_required
def home(request):
    if request.user.is_authenticated:

        user_categories = TransactionCategory.objects.filter(user__id=request.user.id)

        user_transactions = Transaction.objects.filter(user__id=request.user.id)

        context = {
            'categories': user_categories,
            'transactions': user_transactions,
        }

        return render(request, "finance/home.html", context)
    else:
        return redirect('accounts/login')

@login_required
def profile(request):

    return render(request, "finance/profile.html")


class ProfileView(EmailView):
    template_name = 'finance/profile.html'
    success_url = reverse_lazy('profileview')