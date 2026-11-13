from django import forms
from allauth.account.forms import SignupForm, LoginForm, AddEmailForm
from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    first_name = forms.CharField(max_length=32, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=32, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))

    
    def save(self, request):
        user = super().save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user

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