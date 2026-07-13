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

    if request.method == "POST":

        full_name = request.POST["full_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("trekker_register")

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("trekker_register")

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("trekker_register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        user.save()

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect("trekker_login")

    return render(request, "accounts/trekker_register.html")

def company_register(request):
    return render(request, "accounts/company_register.html")

def trekker_login(request):
    return render(request,"accounts/trekker_login.html")

def company_login(request):
    return render(request, "accounts/company_login.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def trekker_register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"],
        username = request.POST["username"],
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
             messages.error(request, "Passwords do not match.")
             return redirect("trekker_register")
        
        if User.objects.filter(username=username).exists():
             messages.error(request, "Username already exists.")
             return redirect("trekker_register")
        if User.objects.filter(email=email).exists():
             messages.error(request, "Email already exists.")
             return redirect("trekker_register")
        # Create the user
        user = User.objects.create_user(
             username=username,
             email=email,
             password=password,
             first_name=full_name
             )

        user.save()


        messages.success(
        request,
        "Registration successful! Please login."
        )

        return redirect("trekker_login")
    return render(request, "accounts/trekker_register.html")