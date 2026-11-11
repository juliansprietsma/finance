from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Welcome {request.user}")
    else:
        return HttpResponse("Please log in")