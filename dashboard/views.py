from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from bookings.models import Booking
from reviews.models import Review


@login_required
def trekker_dashboard(request):

    if hasattr(request.user, "company"):
        return redirect("company_dashboard")

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

    upcoming_booking = (
        Booking.objects.filter(
            trekker=request.user
        )
        .exclude(status__in=["Completed", "Cancelled", "Rejected"])
        .select_related(
            "package",
            "package__company",
            "package__trek",
        )
        .order_by("package__start_date")
        .first()
    )

    context = {
        "booking_count": booking_count,
        "completed_count": completed_count,
        "review_count": review_count,
        "upcoming_booking": upcoming_booking,
    }

    return render(
        request,
        "dashboard/trekker_dashboard.html",
        context,
    )