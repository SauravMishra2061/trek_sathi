from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/admin_dashboard.html")


@login_required
def admin_regions(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/regions.html")


@login_required
def admin_treks(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/treks.html")


@login_required
def admin_companies(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/companies.html")


@login_required
def admin_users(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/users.html")