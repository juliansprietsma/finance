from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.account.views import EmailView, PasswordChangeView
from allauth.account.models import EmailAddress

from django.core.mail import send_mail

from .models import TransactionCategory, Transaction
from .forms import CustomEmailChangeForm, CustomPasswordChangeForm

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