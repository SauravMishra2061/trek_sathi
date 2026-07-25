from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Review


@login_required
def company_reviews(request):

    reviews = Review.objects.filter(
        package__company=request.user.company
    ).select_related(
        "trekker",
        "package"
    ).order_by("-created_at")

    return render(
        request,
        "reviews/company_reviews.html",
        {
            "reviews": reviews,
        },
    )