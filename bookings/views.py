from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from bookings.models import Booking
from bookings.forms import BookingForm
from packages.models import Package
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.utils import timezone
from django.db import transaction

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

    # =====================================
    # COMPANY CANNOT BOOK
    # =====================================

    if hasattr(request.user, "company"):

        messages.error(
            request,
            "Company accounts cannot book trekking packages.",
        )

        return redirect(
            "package_detail",
            pk=package.pk,
        )

    # =====================================
    # DATE VALIDATION
    # =====================================

    today = timezone.localdate()

    if package.end_date < today:

        messages.error(
            request,
            "This trekking package has already ended and cannot be booked.",
        )

        return redirect(
            "package_detail",
            pk=package.pk,
        )

    if package.start_date < today:

        messages.error(
            request,
            "This trekking package has already started and cannot be booked.",
        )

        return redirect(
            "package_detail",
            pk=package.pk,
        )

    # =====================================
    # HANDLE BOOKING
    # =====================================

    if request.method == "POST":

        form = BookingForm(
            request.POST
        )

        if form.is_valid():

            requested_people = (
                form.cleaned_data[
                    "number_of_people"
                ]
            )

            # =====================================
            # PREVENT OVERBOOKING
            # =====================================

            with transaction.atomic():

                # Lock package while booking
                package = (
                    Package.objects
                    .select_for_update()
                    .get(
                        pk=package.pk
                    )
                )

                # Calculate occupied slots
                occupied_slots = (
                    Booking.objects.filter(
                        package=package,
                        status__in=[
                            "Pending",
                            "Approved",
                            "Completed",
                        ],
                    )
                    .aggregate(
                        total=Sum(
                            "number_of_people"
                        )
                    )
                    .get("total")
                    or 0
                )

                # Calculate available slots
                available_slots = max(
                    0,
                    package.max_participants
                    - occupied_slots
                )

                # =====================================
                # PACKAGE FULL
                # =====================================

                if available_slots <= 0:

                    messages.error(
                        request,
                        "Sorry, this package is fully booked.",
                    )

                    return redirect(
                        "package_detail",
                        pk=package.pk,
                    )

                # =====================================
                # TOO MANY PEOPLE REQUESTED
                # =====================================

                if requested_people > available_slots:

                    messages.error(
                        request,
                        (
                            f"Only "
                            f"{available_slots} "
                            f"slot(s) are currently available."
                        ),
                    )

                    return render(
                        request,
                        "bookings/create_booking.html",
                        {
                            "package": package,
                            "form": form,
                            "total_price": (
                                package.price_per_person
                            ),
                            "available_slots": (
                                available_slots
                            ),
                        },
                    )

                # =====================================
                # CREATE BOOKING
                # =====================================

                booking = form.save(
                    commit=False
                )

                booking.trekker = (
                    request.user
                )

                booking.package = (
                    package
                )

                booking.total_price = (
                    package.price_per_person
                    * requested_people
                )

                booking.status = (
                    "Pending"
                )

                booking.save()

            messages.success(
                request,
                "Your booking request was submitted successfully.",
            )

            return redirect(
                "my_bookings"
            )

    else:

        form = BookingForm()

    # =====================================
    # CALCULATE AVAILABLE SLOTS
    # =====================================

    occupied_slots = (
        Booking.objects.filter(
            package=package,
            status__in=[
                "Pending",
                "Approved",
                "Completed",
            ],
        )
        .aggregate(
            total=Sum(
                "number_of_people"
            )
        )
        .get("total")
        or 0
    )

    available_slots = max(
        0,
        package.max_participants
        - occupied_slots
    )

    # =====================================
    # DISPLAY BOOKING PAGE
    # =====================================

    return render(
        request,
        "bookings/create_booking.html",
        {
            "package": package,
            "form": form,
            "total_price": (
                package.price_per_person
            ),
            "available_slots": (
                available_slots
            ),
        },
    )
@login_required
@require_POST
def cancel_booking(request, pk):

    # Get only the current user's booking
    booking = get_object_or_404(
        Booking,
        pk=pk,
        trekker=request.user,
    )

    # Only Pending or Approved bookings can be cancelled
    if booking.status not in ["Pending", "Approved"]:

        messages.error(
            request,
            "This booking cannot be cancelled.",
        )

        return redirect("my_bookings")

    booking.status = "Cancelled"

    booking.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Your booking has been cancelled successfully.",
    )

    return redirect("my_bookings")
