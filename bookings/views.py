from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from bookings.models import Booking
from bookings.forms import BookingForm
from packages.models import Package
from django.contrib import messages
from django.views.decorators.http import require_POST


@login_required
def company_bookings(request):

    bookings = (
        Booking.objects.filter(
            package__company=request.user.company
        )
        .select_related(
            "package",
            "trekker",
        )
        .order_by("-booking_date")
    )

    return render(
        request,
        "bookings/company_bookings.html",
        {
            "bookings": bookings,
        },
    )


@login_required
def booking_detail(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        package__company=request.user.company,
    )

    return render(
        request,
        "bookings/booking_detail.html",
        {
            "booking": booking,
        },
    )
@login_required
@require_POST
def approve_booking(request, pk):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    booking = get_object_or_404(
        Booking,
        pk=pk,
        package__company=request.user.company,
        status="Pending",
    )

    booking.status = "Approved"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        "The booking has been approved successfully.",
    )

    return redirect(
        "booking_detail",
        pk=booking.pk,
    )


@login_required
@require_POST
def reject_booking(request, pk):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    booking = get_object_or_404(
        Booking,
        pk=pk,
        package__company=request.user.company,
        status="Pending",
    )

    booking.status = "Rejected"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        "The booking has been rejected.",
    )

    return redirect(
        "booking_detail",
        pk=booking.pk,
    )


@login_required
@require_POST
def complete_booking(request, pk):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    booking = get_object_or_404(
        Booking,
        pk=pk,
        package__company=request.user.company,
        status="Approved",
    )

    booking.status = "Completed"
    booking.save(update_fields=["status", "updated_at"])

    messages.success(
        request,
        "The booking has been marked as completed.",
    )

    return redirect(
        "booking_detail",
        pk=booking.pk,
    )

@login_required
def create_booking(request, package_id):

    package = get_object_or_404(
        Package,
        pk=package_id,
        status="Published",
    )

    if hasattr(request.user, "company"):
        messages.error(
            request,
            "Company accounts cannot book trekking packages.",
        )
        return redirect(
            "package_detail",
            pk=package.pk,
        )

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.trekker = request.user
            booking.package = package
            booking.total_price = (
                package.price_per_person
                * booking.number_of_people
            )
            booking.save()

            messages.success(
                request,
                "Your booking request was submitted successfully.",
            )

            return redirect("my_bookings")
    else:
        form = BookingForm()

    return render(
        request,
        "bookings/create_booking.html",
        {
            "package": package,
            "form": form,
            "total_price": package.price_per_person,
        },
    )
