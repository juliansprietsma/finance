from django import forms
from allauth.account.forms import SignupForm, LoginForm, AddEmailForm, ChangePasswordForm, ResetPasswordForm
from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import TransactionCategory


class TransactionCategoryForm(ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['category', 'budget']
        widgets = {
            'category': forms.TextInput(attrs={"class": "form-control"}),
            'budget': forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_category(self):
        category = self.cleaned_data['category'].strip()

        if TransactionCategory.objects.filter(user=self.user, category__iexact=category).exists():
            raise forms.ValidationError("You already have a category with this name")

        return category

    def save(self, commit=True):
        category = super().save(commit=False)
        category.user = self.user
        if commit:
            category.save()
        return category


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    first_name = forms.CharField(max_length=32, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=32, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))

    def clean_email(self):
        email = super().clean_email()

        if EmailAddress.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email address is already being used by another account.")

        return super().clean_email()

    def save(self, request):
        user = super().save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user

class CustomPasswordResetForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def clean_email(self):
        return super().clean_email()

    def save(self, request):
        return super().save(request)

    
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def login(self, request, redirect_url=None):
        return super().login(request, redirect_url)


class CustomEmailChangeForm(AddEmailForm):
    def clean_email(self):
        email = super().clean_email()

        if EmailAddress.objects.filter(email__iexact=email).exclude(user=self.user).exists():
            raise ValidationError("This email address is already being used by another account.")

        return super().clean_email()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, request):
        return super().save(request)


class CustomPasswordChangeForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self):
        super().save()