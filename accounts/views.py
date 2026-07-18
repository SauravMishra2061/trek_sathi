from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from companies.models import Company

from .forms import ProfileForm, UserForm  # adjust import path if needed


def login_choice(request):
    return render(request, "accounts/login_choice.html")


def register_choice(request):
    return render(request, "accounts/register_choice.html")


def company_register(request):
    if request.method == "POST":

        company_name = request.POST["company_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        registration_number = request.POST["registration_number"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("company_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("company_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("company_register")

        if Company.objects.filter(registration_number=registration_number).exists():
            messages.error(request, "Registration number already exists.")
            return redirect("company_register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=company_name
        )

        Company.objects.create(
            user=user,
            company_name=company_name,
            phone=phone,
            registration_number=registration_number
        )

        messages.success(request, "Company registered successfully. Please login.")
        return redirect("company_login")

    return render(request, "accounts/company_register.html")

def company_login(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            # Only company accounts are allowed
            if not hasattr(user, "company"):
                messages.error(request, "Please use the Trekker Login.")
                return redirect("company_login")

            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("company_dashboard")

        messages.error(request, "Invalid username or password.")
        return redirect("company_login")

    return render(request, "accounts/company_login.html")

def trekker_register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        username = request.POST["username"]
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

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("trekker_login")

    return render(request, "accounts/trekker_register.html")

def trekker_login(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            # Prevent company accounts from logging in here
            if hasattr(user, "company"):
                messages.error(request, "Please use the Company Login.")
                return redirect("trekker_login")

            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("home")

        messages.error(request, "Invalid username or password.")
        return redirect("trekker_login")

    return render(request, "accounts/trekker_login.html")
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")


@login_required
def profile(request):
    profile = request.user.profile
    edit = request.GET.get("edit") == "true"

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

        edit = True
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {
        "profile": profile,
        "user_form": user_form,
        "profile_form": profile_form,
        "edit": edit,
    }

    return render(request, "home/profile.html", context)
from django.contrib.auth.decorators import login_required

@login_required
def my_bookings(request):
    return render(request, "home/my_bookings.html")

@login_required
def saved_packages(request):
    return render(request, "home/saved_packages.html")