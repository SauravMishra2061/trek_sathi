from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def company_dashboard(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_dashboard.html")


@login_required
def company_packages(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_packages.html")


@login_required
def company_bookings(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_bookings.html")


@login_required
def company_messages(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_messages.html")


@login_required
def company_earnings(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_earnings.html")


@login_required
def company_reviews(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_reviews.html")


@login_required
def company_profile(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_profile.html")