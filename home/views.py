from django.shortcuts import render, redirect
from django.utils import timezone

from packages.models import Package
from regions.models import Region

def home(request):


# =====================================
# REDIRECT ONLY ADMIN USERS
# =====================================

    if (
        request.user.is_authenticated
        and (
            request.user.is_superuser
            or request.user.is_staff
        )
    ):
        return redirect("admin_dashboard")

    # =====================================
    # PUBLIC HOMEPAGE
    # =====================================

    today = timezone.localdate()

    latest_packages = (
        Package.objects.filter(
            status="Published",
            end_date__gte=today,
        )
        .select_related(
            "company",
            "trek",
            "trek__region",
        )
        .order_by("-created_at")[:3]
    )

    regions = (
        Region.objects.filter(
            is_active=True
        )
        .order_by("name")
    )

    return render(
        request,
        "home/index.html",
        {
            "latest_packages": latest_packages,
            "regions": regions,
        },
    )


def profile(request):


    return render(
        request,
        "home/profile.html"
    )

