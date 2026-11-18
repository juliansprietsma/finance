from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.db.models.functions import Lower

import datetime

from allauth.account.views import EmailView, PasswordChangeView
from allauth.account.models import EmailAddress

from django.core.mail import send_mail

from .models import TransactionCategory, Transaction
from .forms import CustomEmailChangeForm, CustomPasswordChangeForm, CreateTransactionCategoryForm, CreateTransactionForm

EDIT_TX_ID = "edit_tx_%s"

# Create your views here.
@login_required
def home(request, year: int | None = None, month: int | None = None):
    if request.user.is_authenticated:

        if (month and year) and (month >= 1 and month <= 12) and (year >= 0 and year <= datetime.datetime.now().year + 5):
            year = year
            month = month
        else:
            year=datetime.datetime.now().year
            month=datetime.datetime.now().month

        selected_categories = [c.lower() for c in request.GET.getlist("category")]

        print(selected_categories)

        month_filter = datetime.date(year=year, month=month, day=1)
        user_categories = TransactionCategory.objects.filter(user__id=request.user.id)
        user_transactions = Transaction.objects.filter(user__id=request.user.id, date__year=month_filter.year, date__month=month_filter.month)
        if selected_categories:
            user_transactions = user_transactions.annotate(category_lower=Lower("category__category")).filter(category_lower__in=selected_categories)

        user_expenses = user_transactions.filter(type='expense', user=request.user, category__budget__gt=0)
        spent_per_category = list(user_expenses.values('category__category').annotate(spent=Sum('amount')).order_by('-spent'))

        for item in spent_per_category:
            item['budget'] = TransactionCategory.objects.filter(category=item['category__category']).values('budget').first()['budget']
            item['percentage_spent'] = item['spent'] / item['budget'] * 100

        category_filter = list(user_categories)
        for cat in category_filter:
            cat.active = cat.category.lower() in selected_categories

        context = {
            'categories': category_filter,
            'transactions': user_transactions,
            'category_create_form': CreateTransactionCategoryForm(user=request.user),
            'transaction_create_form': CreateTransactionForm(user=request.user),
            'spent_per_category': spent_per_category,
            'year': year,
            'month': month,
        }

        return render(request, "finance/home.html", context)
    else:
        return redirect('accounts/login')

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == "POST":
        form = CreateTransactionForm(request.POST, user=request.user, instance=transaction, auto_id=EDIT_TX_ID)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        
        return render(request, "finance/forms/create_transaction_form.html", {"transaction_create_form": form}, status=400)
    
    form = CreateTransactionForm(instance=transaction, user=request.user, auto_id=EDIT_TX_ID)
    return render(request, "finance/forms/create_transaction_form.html", {"transaction_create_form": form})

@login_required
@require_POST
def add_transaction(request):
    form = CreateTransactionForm(request.POST, user=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True})
    return render(request, "finance/forms/create_transaction_form.html", {'transaction_create_form': form}, status=400)

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if not type(transaction) == Transaction:
        return redirect('/')

    transaction.delete()
    return redirect('/')

@login_required
def edit_category(request, pk):
    category = get_object_or_404(TransactionCategory, pk=pk, user=request.user)

    if request.method == "POST":
        form = CreateTransactionCategoryForm(request.POST, user=request.user, instance=category)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        return render(request, "finance/forms/create_category_form.html", {"category_create_form": form}, status=400)

    form = CreateTransactionCategoryForm(instance=category, user=request.user)
    return render(request, "finance/forms/create_category_form.html", {"category_create_form": form})

@login_required
@require_POST
def add_transaction_category(request):
    form = CreateTransactionCategoryForm(request.POST, user=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True})
    return render(request, "finance/forms/create_category_form.html", {'category_create_form': form}, status=400)

@login_required
def delete_transaction_category(request, pk):
    category = get_object_or_404(TransactionCategory, pk=pk, user=request.user)

    if not isinstance(category, TransactionCategory):
        return redirect('/')

    category.delete()
    return redirect('/')

@login_required
def profile(request):
    return render(request, "finance/profile.html")

class ProfilePasswordChangeView(PasswordChangeView):
    template_name = 'finance/profile/html'
    success_url = reverse_lazy('profileview')

class ProfileEmailChangeView(EmailView):
    template_name = 'finance/profile/html'
    success_url = reverse_lazy('profileview')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/profile.html'
    success_url = reverse_lazy('profileview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["email_form"] = kwargs.get(
            "email_form",
            CustomEmailChangeForm(self.request.user)
        )

        context["password_form"] = kwargs.get(
            "password_change_form",
            CustomPasswordChangeForm(self.request.user)
        )

        context["emailaddresses"] = EmailAddress.objects.filter(user=self.request.user)
        context["current_emailaddress"] = EmailAddress.objects.get_verified(self.request.user)
        context["new_emailaddress"] = EmailAddress.objects.get_new(self.request.user)


        return context

    def post(self, request, *args, **kwargs):
        if "change_email" in request.POST:
            form = CustomEmailChangeForm(request.user, data=request.POST)

            if form.is_valid():
                form.save(request)
                return redirect("profileview")

            return self.render_to_response(
                self.get_context_data(email_form=form)
            )

        if "change_password" in request.POST:
            form = CustomPasswordChangeForm(request.user, data=request.POST)

            if form.is_valid():
                form.save()
                return redirect("profileview")

            return self.render_to_response(
                self.get_context_data(password_change_form=form)
            )

        return redirect("profileview")
