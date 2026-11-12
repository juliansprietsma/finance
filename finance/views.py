from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:

        return render(request, "finance/home.html", {"message": f"Hello {request.user.first_name}"})
    else:
        return render(request, "finance/home.html", {"message": f"Please log in"})