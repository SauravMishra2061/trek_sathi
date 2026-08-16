from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from companies.models import Company

from .forms import ProfileForm, UserForm  # adjust import path if needed
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re

def login_choice(request):
    return render(request, "accounts/login_choice.html")


def register_choice(request):
    return render(request, "accounts/register_choice.html")

def company_register(request):
    if request.method == "POST":

        company_name = request.POST.get("company_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        registration_number = request.POST.get(
            "registration_number", ""
        ).strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Values to preserve after an error
        context = {
            "company_name": company_name,
            "username": username,
            "email": email,
            "phone": phone,
            "registration_number": registration_number,
        }

        # Company name validation
        if not company_name:
            messages.error(request, "Company name is required.")
            context["company_name"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if len(company_name) < 2:
            messages.error(
                request,
                "Company name must be at least 2 characters long."
            )
            context["company_name"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Username validation
        if not username:
            messages.error(request, "Username is required.")
            context["username"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if len(username) < 4:
            messages.error(
                request,
                "Username must be at least 4 characters long."
            )
            context["username"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            messages.error(
                request,
                "Username can only contain letters, numbers, and underscores."
            )
            context["username"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists.")
            context["username"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Email validation
        if not email:
            messages.error(request, "Email is required.")
            context["email"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already exists.")
            context["email"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Phone validation
        if not phone:
            messages.error(request, "Phone number is required.")
            context["phone"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if not re.fullmatch(r"\+?[0-9]+", phone):
            messages.error(
                request,
                "Phone number can only contain numbers and an optional + sign."
            )
            context["phone"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if len(phone) > 14:
            messages.error(
                request,
                "Phone number cannot be longer than 14 characters."
            )
            context["phone"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Registration number validation
        if not registration_number:
            messages.error(
                request,
                "Government registration number is required."
            )
            context["registration_number"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if Company.objects.filter(
            registration_number__iexact=registration_number
        ).exists():
            messages.error(
                request,
                "Registration number already exists."
            )
            context["registration_number"] = ""
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Password validation
        if not password:
            messages.error(request, "Password is required.")
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if not confirm_password:
            messages.error(
                request,
                "Please confirm your password."
            )
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Django password validators
        try:
            validate_password(
                password,
                user=User(
                    username=username,
                    email=email,
                    first_name=company_name,
                )
            )
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)

            return render(
                request,
                "accounts/company_register.html",
                context
            )

        # Create company account only after all validation passes
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

        messages.success(
            request,
            "Company registered successfully. Please login."
        )

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
            login(request, user)
            if user.is_staff:
                return redirect("admin_dashboard")
            # Only company accounts are allowed
            if not hasattr(user, "company"):
                messages.error(request, "Please use the Trekker Login.")
                return redirect("company_login")

            
            messages.success(request, "Welcome back!")
            return redirect("company_dashboard")

        messages.error(request, "Invalid username or password.")
        return redirect("company_login")

    return render(request, "accounts/company_login.html")

def trekker_register(request):
    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Values to keep after an error
        context = {
            "full_name": full_name,
            "username": username,
            "email": email,
            "phone": phone,
        }

        # Full name validation
        if not full_name:
            messages.error(request, "Full name is required.")
            context["full_name"] = ""
            return render(request, "accounts/trekker_register.html", context)

        if len(full_name) < 2:
            messages.error(request, "Full name must be at least 2 characters long.")
            context["full_name"] = ""
            return render(request, "accounts/trekker_register.html", context)

        # Username validation
        if not username:
            messages.error(request, "Username is required.")
            context["username"] = ""
            return render(request, "accounts/trekker_register.html", context)

        if len(username) < 4:
            messages.error(request, "Username must be at least 4 characters long.")
            context["username"] = ""
            return render(request, "accounts/trekker_register.html", context)

        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            messages.error(
                request,
                "Username can only contain letters, numbers, and underscores."
            )
            context["username"] = ""
            return render(request, "accounts/trekker_register.html", context)

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists.")
            context["username"] = ""
            return render(request, "accounts/trekker_register.html", context)

        # Email validation
        if not email:
            messages.error(request, "Email is required.")
            context["email"] = ""
            return render(request, "accounts/trekker_register.html", context)

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already exists.")
            context["email"] = ""
            return render(request, "accounts/trekker_register.html", context)

        # Phone UX/backend format validation
        if phone and not re.fullmatch(r"\+?[0-9]+", phone):
            messages.error(
                request,
                "Phone number can only contain numbers and an optional + sign."
            )
            context["phone"] = ""
            return render(request, "accounts/trekker_register.html", context)

        if phone and len(phone) > 14:
            messages.error(
                request,
                "Phone number cannot be longer than 14 characters."
            )
            context["phone"] = ""
            return render(request, "accounts/trekker_register.html", context)

        # Password validation
        if not password:
            messages.error(request, "Password is required.")
            return render(request, "accounts/trekker_register.html", context)

        if not confirm_password:
            messages.error(request, "Please confirm your password.")
            return render(request, "accounts/trekker_register.html", context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/trekker_register.html", context)

        try:
            validate_password(
                password,
                user=User(
                    username=username,
                    email=email,
                    first_name=full_name,
                )
            )
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)

            return render(request, "accounts/trekker_register.html", context)

        # Create user only after ALL validation passes
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
        )

        # Profile is automatically created by the User post_save signal.
        # Save the phone number if the user provided one.
        if phone:
            user.profile.phone = phone
            user.profile.save()

        messages.success(
            request,
            "Registration successful! Please login."
        )

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
            login(request, user)
            if user.is_staff:
                return redirect("admin_dashboard")

            # Prevent company accounts from logging in here
            if hasattr(user, "company"):
                messages.error(request, "Please use the Company Login.")
                return redirect("trekker_login")

            
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