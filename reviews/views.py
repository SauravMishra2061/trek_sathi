from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from bookings.models import Booking

from .models import Review
from .forms import ReviewForm


@login_required
def company_reviews(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    reviews = (
        Review.objects.filter(
            package__company=request.user.company
        )
        .select_related(
            "trekker",
            "package",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "reviews/company_reviews.html",
        {
            "reviews": reviews,
        },
    )


@login_required
def create_review(request, booking_id):

    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        trekker=request.user,
        status="Completed",
    )

    # Prevent duplicate reviews
    if hasattr(booking, "review"):

        messages.info(
            request,
            "You have already submitted a review for this booking.",
        )

        return redirect("my_bookings")

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.trekker = request.user
            review.package = booking.package
            review.booking = booking

            review.save()

            messages.success(
                request,
                "Your rating has been submitted successfully.",
            )

            return redirect("my_bookings")

    else:

        form = ReviewForm()

    return render(
        request,
        "reviews/create_reviews.html",
        {
            "booking": booking,
            "form": form,
        },
    )