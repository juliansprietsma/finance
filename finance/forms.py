from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
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