from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from companies.models import TrekRequest
from django.shortcuts import get_object_or_404
from adminpanel.forms import TrekRequestReviewForm
from treks.models import Trek
from django.contrib import messages
from .forms import TrekRequestReviewForm


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/admin_dashboard.html")


@login_required
def admin_regions(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/regions.html")


@login_required
def admin_treks(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/treks.html")


@login_required
def admin_companies(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/companies.html")


@login_required
def admin_users(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    return render(request, "adminpanel/users.html")
from django.db.models import Q

@login_required
def trek_requests(request):

    search = request.GET.get("search")
    status = request.GET.get("status")

    requests = TrekRequest.objects.select_related(
        "company",
        "region"
    )

    if search:
        requests = requests.filter(
            Q(trek_name__icontains=search) |
            Q(company__company_name__icontains=search)
        )

    if status:
        requests = requests.filter(status=status)

    requests = requests.order_by("-created_at")

    return render(
        request,
        "adminpanel/trek_requests.html",
        {
            "requests": requests,
            "search": search,
            "status": status,
        },
    )
@login_required
def review_trek_request(request, pk):

    trek_request = get_object_or_404(
        TrekRequest,
        pk=pk
    )

    if request.method == "POST":

        form = TrekRequestReviewForm(request.POST)

        if form.is_valid():

            feedback = form.cleaned_data["admin_feedback"]

            action = request.POST.get("action")

            if action == "approve":
                if trek_request.status != "Pending":
                    messages.warning(
                    request,
                    "This request has already been reviewed."
                    )
                    return redirect("admin_trek_requests")

                trek, created = Trek.objects.get_or_create(
                    name=trek_request.trek_name,
                    region=trek_request.region,
                    defaults={
                    "description": trek_request.description,
                    "altitude": trek_request.estimated_altitude,
                    "difficulty": trek_request.difficulty,
                    "image": trek_request.reference_image,
                    "is_active": True,
                    },
                )

                trek_request.status = "Approved"

                trek_request.admin_feedback = feedback

                trek_request.save()

                messages.success(
                    request,
                    "Trek request approved successfully."
                )

            elif action == "reject":

                trek_request.status = "Rejected"

                trek_request.admin_feedback = feedback

                trek_request.save()

                messages.success(
                    request,
                    "Trek request rejected."
                )

            return redirect("admin_trek_requests")

    else:

        form = TrekRequestReviewForm(
            initial={
                "admin_feedback": trek_request.admin_feedback
            }
        )

    return render(
        request,
        "adminpanel/review_trek_request.html",
        {
            "request_obj": trek_request,
            "form": form,
        },
    )