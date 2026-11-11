from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:

        return render(request, "finance/home.html", {"user": request.user})
    else:
        return render(request, "finance/login.html")