from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from allauth.account.views import EmailView, PasswordChangeView
from allauth.account.models import EmailAddress

from django.core.mail import send_mail

from .models import TransactionCategory, Transaction
from .forms import CustomEmailChangeForm, CustomPasswordChangeForm, TransactionCategoryForm

# Create your views here.
@login_required
def home(request):
    if request.user.is_authenticated:

        user_categories = TransactionCategory.objects.filter(user__id=request.user.id)

        user_transactions = Transaction.objects.filter(user__id=request.user.id)

        context = {
            'categories': user_categories,
            'transactions': user_transactions,
            'category_create_form': TransactionCategoryForm(user=request.user),
        }

        return render(request, "finance/home.html", context)
    else:
        return redirect('accounts/login')

@login_required
@require_POST
def add_transaction_category(request):
    form = TransactionCategoryForm(request.POST, user=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True})
    return render(request, "finance/forms/transaction_form.html", {'category_create_form': form}, status=400)


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

