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
        .exclude(
           status__in=["Completed", "Cancelled", "Rejected"]
        )
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
@login_required
def my_bookings(request):

    if hasattr(request.user, "company"):
        return redirect("company_dashboard")

    bookings = (
        Booking.objects.filter(trekker=request.user)
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