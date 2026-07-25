from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bookings.models import Booking



@login_required
def company_bookings(request):

    bookings = Booking.objects.filter(
        package__company=request.user.company
    ).select_related(
        "package",
        "trekker"
    ).order_by("-booking_date")

    return render(
        request,
        "bookings/company_bookings.html",
        {
            "bookings": bookings,
        },
    )
from django.shortcuts import get_object_or_404


@login_required
def booking_detail(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        package__company=request.user.company
    )

    return render(
        request,
        "bookings/booking_detail.html",
        {
            "booking": booking,
        },
    )
