from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from bookings.models import Booking
from reviews.models import Review
from packages.models import SavedPackage


@login_required
def trekker_dashboard(request):

    # Redirect company users
    if hasattr(request.user, "company"):
        return redirect("company_dashboard")

    # ==========================================
    # DASHBOARD STATISTICS
    # ==========================================

    booking_count = Booking.objects.filter(
        trekker=request.user
    ).count()

    completed_count = Booking.objects.filter(
        trekker=request.user,
        status="Completed"
    ).count()

    review_count = Review.objects.filter(
        trekker=request.user
    ).count()


    # ==========================================
    # BOOKINGS
    # ==========================================

    bookings = (
        Booking.objects.filter(
            trekker=request.user
        )
        .select_related(
            "package",
            "package__company",
            "package__trek",
            "package__trek__region",
        )
        .order_by("-booking_date")
    )

    today = timezone.localdate()

    upcoming_bookings = (
        bookings
        .exclude(
            status__in=[
                "Completed",
                "Cancelled",
                "Rejected",
            ]
        )
        .filter(
            package__start_date__gte=today
        )
        .order_by("package__start_date")
    )

    upcoming_treks = upcoming_bookings[:3]

    recent_bookings = bookings[:3]

    upcoming_booking = upcoming_bookings.first()


    # ==========================================
    # SAVED PACKAGES
    # ==========================================

    saved_packages = (
    SavedPackage.objects.filter(
        trekker=request.user,
        package__status="Published",
        package__start_date__gt=today,
        package__end_date__gte=today,
    )
    .select_related(
        "package",
        "package__company",
        "package__trek",
        "package__trek__region",
    )
    .order_by("-saved_at")[:3]
    )


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {
        "booking_count": booking_count,
        "completed_count": completed_count,
        "review_count": review_count,

        "upcoming_booking": upcoming_booking,
        "upcoming_bookings": upcoming_bookings[:3],
        "upcoming_treks": upcoming_treks,
        "recent_bookings": recent_bookings,

        # Saved packages for dashboard
        "saved_packages": saved_packages,
    }


    return render(
        request,
        "dashboard/trekker_dashboard.html",
        context,
    )
@login_required
def my_bookings(request):

    if hasattr(request.user, "company"):
        return redirect("company_dashboard")

    bookings = (
        Booking.objects.filter(
            trekker=request.user
        )
        .select_related(
            "package",
            "package__company",
            "package__trek",
            "package__trek__region",
        )
        .order_by("-booking_date")
    )

    active_bookings = bookings.exclude(
        status__in=["Completed", "Cancelled"]
    )

    completed_bookings = bookings.filter(
        status="Completed"
    )

    context = {
        "bookings": bookings,
        "active_bookings": active_bookings,
        "completed_bookings": completed_bookings,
    }

    return render(
        request,
        "bookings/my_bookings.html",
        context,
    )