from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from .models import Company
from django.contrib import messages
from .forms import CompanyFeedbackForm
from .forms import CompanyProfileForm
from .forms import CompanyDocumentForm
from bookings.models import Booking
from packages.models import Package
from django.db.models import Sum, F
from reviews.models import Review
from .forms import TrekRequestForm
from .models import TrekRequest
from django.contrib import messages



@login_required
def company_dashboard(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    package_count = Package.objects.filter(
        company=company
    ).count()

    published_packages = Package.objects.filter(
        company=company,
        status="Published"
    ).count()

    booking_count = Booking.objects.filter(
        package__company=company
    ).count()

    estimated_revenue = (
        Booking.objects.filter(package__company=company)
        .aggregate(total=Sum(F("package__price_per_person")))
    )["total"] or 0

    # Temporary until Review model is connected
    review_count = 0
    average_rating = 0

    context = {

        "company": company,

        "show_approval_popup": (
            company.status == "Approved"
            and not company.approval_message_seen
        ),

        "package_count": package_count,
        "published_packages": published_packages,
        "booking_count": booking_count,
        "review_count": review_count,
        "average_rating": average_rating,
        "estimated_revenue": estimated_revenue,

    }
    recent_bookings = Booking.objects.filter(
       package__company=company
        ).select_related(
        "trekker",
        "package"
        ).order_by("-booking_date")[:5]

    recent_reviews = (
        Review.objects.filter(
        package__company=company
        )
        .select_related(
        "trekker",
        "package"
        )
        .order_by("-created_at")[:5]
    )

    return render(
        request,
        "companies/company_dashboard.html",
        context,
    )
@login_required
def company_packages(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    if company.status != "Approved":
        messages.error(
            request,
            "Your company must be approved before you can manage packages."
        )
        return redirect("company_dashboard")

    return render(
        request,
        "companies/company_packages.html"
    )
@login_required
def company_bookings(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_bookings.html")


@login_required
def company_messages(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_messages.html")


@login_required
def company_earnings(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    return render(request, "companies/company_earnings.html")

@login_required
def company_reviews(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    reviews = (
        Review.objects
        .filter(package__company=company)
        .select_related("trekker", "package", "package__trek")
        .order_by("-created_at")
    )

    return render(
        request,
        "companies/company_reviews.html",
        {
            "company": company,
            "reviews": reviews,
        },
    )


@login_required
def company_profile(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    return render(request,"companies/company_profile.html",{"company": company,},)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Company


def company_list(request):

    companies = Company.objects.select_related("user").all()

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        companies = companies.filter(
            company_name__icontains=search
        )

    if status:
        companies = companies.filter(
            status=status
        )

    companies = companies.order_by("-created_at")

    return render(
        request,
        "companies/company_list.html",
        {
            "companies": companies,
            "search": search,
            "status": status,
        }
    )


def company_detail(request, pk):

    company = get_object_or_404(Company, pk=pk)

    return render(
        request,
        "companies/company_detail.html",
        {
            "company": company
        }
    )


def approve_company(request, pk):

    company = get_object_or_404(Company, pk=pk)

    company.status = "Approved"
    company.approval_message_seen = False
    company.save()

    messages.success(
    request,
    f"{company.company_name} has been approved successfully."
    )

    return redirect("company_list")

   


def reject_company(request, pk):

    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":

        form = CompanyFeedbackForm(request.POST, instance=company)

        if form.is_valid():

            company = form.save(commit=False)
            company.status = "Rejected"
            company.save()

            messages.warning(
                request,
                f"{company.company_name} has been rejected."
            )

            return redirect("company_detail", pk=company.pk)

    else:

        form = CompanyFeedbackForm(instance=company)

    return render(
        request,
        "companies/company_status_form.html",
        {
            "company": company,
            "form": form,
            "title": "Reject Company",
            "subtitle": "Provide a reason for rejection.",
            "button_text": "Reject",
            "button_class": "reject-btn",
            "button_icon": "fa-solid fa-xmark",
            "show_feedback": True,
        },
    )


def suspend_company(request, pk):

    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":

        form = CompanyFeedbackForm(request.POST, instance=company)

        if form.is_valid():

          company = form.save(commit=False)
          company.status = "Suspended"
          company.save()

          messages.error(
            request,
            f"{company.company_name} has been suspended."
            )

          return redirect("company_detail", pk=company.pk)

    else:

        form = CompanyFeedbackForm(instance=company)

    return render(
        request,
        "companies/company_status_form.html",
        {
            "company": company,
            "form": form,
            "title": "Suspend Company",
            "subtitle": "Provide a reason for suspension.",
            "button_text": "Suspend",
            "button_class": "suspend-btn",
            "button_icon": "fa-solid fa-ban",
            "show_feedback": True,
        },
    )


@login_required
def dismiss_approval_message(request):

    company = request.user.company

    company.approval_message_seen = True

    company.save()

    return redirect("company_dashboard")

@login_required
def company_verification(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    return render(
        request,
        "companies/company_verification.html",
        {
            "company": company,
        },
    )
@login_required
def edit_company_profile(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    if request.method == "POST":

        form = CompanyProfileForm(
            request.POST,
            request.FILES,
            instance=company,
        )

        if form.is_valid():

            updated_company = form.save()

            # Keep Django User email synchronized
            request.user.email = updated_company.email or ""
            request.user.save(update_fields=["email"])

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("company_profile")

    else:

        form = CompanyProfileForm(instance=company)

    return render(
        request,
        "companies/edit_company_profile.html",
        {
            "form": form,
            "company": company,
        },
    )
@login_required
def replace_company_document(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    if request.method == "POST":

        form = CompanyDocumentForm(
            request.POST,
            request.FILES,
            instance=company,
        )

        if form.is_valid():

            company = form.save(commit=False)

            # Reset verification
            company.status = "Pending"
            company.admin_feedback = ""
            company.approval_message_seen = False

            company.save()

            messages.success(
                request,
                "Your new document has been submitted for verification."
            )

            return redirect("company_verification")

    else:

        form = CompanyDocumentForm(instance=company)

    return render(
        request,
        "companies/replace_document.html",
        {
            "form": form,
            "company": company,
        },
    )
@login_required
def trek_requests(request):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    requests = company.trek_requests.all().order_by("-id")

    if request.method == "POST":

        form = TrekRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            trek_request = form.save(commit=False)

            trek_request.company = company

            trek_request.save()

            messages.success(
                request,
                "Your trek request has been submitted successfully."
            )

            return redirect("trek_requests")

    else:

        form = TrekRequestForm()

    return render(
        request,
        "companies/trek_requests.html",
        {
            "form": form,
            "requests": requests,
        },
    )