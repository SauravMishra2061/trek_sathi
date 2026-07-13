from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def login_choice(request):
    return render(request, "accounts/login_choice.html")

from django.shortcuts import render

def register_choice(request):
    return render(request, "accounts/register_choice.html")

from django.shortcuts import render

def trekker_register(request):
    return render(request, "accounts/trekker_register.html")

def company_register(request):
    return render(request, "accounts/company_register.html")