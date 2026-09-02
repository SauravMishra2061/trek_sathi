from django.shortcuts import render
from django.utils import timezone

from packages.models import Package
from regions.models import Region


def home(request):

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
