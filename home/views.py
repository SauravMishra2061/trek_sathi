from django.shortcuts import render

def home(request):
    return render(request, "home/index.html")

def profile(request):
    return render(request, "home/profile.html")