from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from .models import Company
from django.contrib import messages
from .forms import CompanyFeedbackForm
from .forms import CompanyProfileForm
from .forms import CompanyDocumentForm
from bookings.models import Booking
from packages.models import Package
from django.db.models import Sum, F, Count, Q
from reviews.models import Review
from .forms import TrekRequestForm
from .models import TrekRequest
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)



@login_required
def company_dashboard(request):

    # Prevent trekkers or other users from accessing company dashboard
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    # -------------------------------------------------
    # COMPANY PACKAGES
    # Only packages belonging to the logged-in company
    # -------------------------------------------------

    packages = Package.objects.filter(company=company)

    package_stats = packages.aggregate(
        total_packages=Count("id"),
        published_packages=Count(
            "id",
            filter=Q(status="Published")
        ),
        draft_packages=Count(
            "id",
            filter=Q(status="Draft")
        ),
    )

    # -------------------------------------------------
    # COMPANY BOOKINGS
    # Only bookings belonging to this company's packages
    # -------------------------------------------------

    bookings = Booking.objects.filter(
        package__company=company
    )

    booking_stats = bookings.aggregate(
        total_bookings=Count("id"),

        pending_bookings=Count(
            "id",
            filter=Q(status="Pending")
        ),

        approved_bookings=Count(
            "id",
            filter=Q(status="Approved")
        ),

        completed_bookings=Count(
            "id",
            filter=Q(status="Completed")
        ),

        cancelled_bookings=Count(
            "id",
            filter=Q(status="Cancelled")
        ),

        rejected_bookings=Count(
            "id",
            filter=Q(status="Rejected")
        ),

        # Count unique trekkers who booked this company's packages
        total_trekkers=Count(
            "trekker",
            distinct=True
        ),
    )

    # -------------------------------------------------
    # ESTIMATED REVENUE
    # Keeping your existing functionality
    # -------------------------------------------------

    estimated_revenue = (
        bookings.aggregate(
            total=Sum(F("package__price_per_person"))
        )["total"]
        or 0
    )

    # -------------------------------------------------
    # RECENT BOOKINGS
    # Latest 5 bookings for this company only
    # -------------------------------------------------

    recent_bookings = (
        bookings
        .select_related(
            "trekker",
            "package"
        )
        .order_by("-booking_date")[:5]
    )

    # -------------------------------------------------
    # RECENT REVIEWS
    # Keeping existing functionality
    # -------------------------------------------------

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

    # Temporary until Review statistics are connected
    review_count = 0
    average_rating = 0

    # -------------------------------------------------
    # TEMPLATE CONTEXT
    # -------------------------------------------------

    context = {

        "company": company,

        "show_approval_popup": (
            company.status == "Approved"
            and not company.approval_message_seen
        ),

        # Package statistics
        "package_count": package_stats["total_packages"],
        "published_packages": package_stats["published_packages"],
        "draft_packages": package_stats["draft_packages"],

        # Booking statistics
        "booking_count": booking_stats["total_bookings"],
        "pending_bookings": booking_stats["pending_bookings"],
        "approved_bookings": booking_stats["approved_bookings"],
        "completed_bookings": booking_stats["completed_bookings"],
        "cancelled_bookings": booking_stats["cancelled_bookings"],
        "rejected_bookings": booking_stats["rejected_bookings"],

        # Unique trekkers/customers
        "total_trekkers": booking_stats["total_trekkers"],

        # Existing statistics
        "estimated_revenue": estimated_revenue,
        "review_count": review_count,
        "average_rating": average_rating,

        # Recent activity
        "recent_bookings": recent_bookings,
        "recent_reviews": recent_reviews,
    }

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
@login_required
def generate_company_report(request):


# =====================================
# SECURITY CHECK
# Only company users can access this view
# =====================================

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company


# =====================================
# COMPANY PACKAGES ONLY
# =====================================

    packages = (
        Package.objects
        .filter(company=company)
        .select_related("trek")
        .order_by("-created_at")
    )


# =====================================
# COMPANY BOOKINGS ONLY
#
# Security:
# Booking -> Package -> Company
# =====================================

    bookings = (
        Booking.objects
        .filter(package__company=company)
        .select_related(
            "package",
            "package__trek",
            "trekker",
        )
        .order_by("-booking_date")
    )


# =====================================
# PACKAGE STATISTICS
# =====================================

    package_stats = packages.aggregate(

        total_packages=Count("id"),

        published_packages=Count(
            "id",
            filter=Q(status="Published"),
        ),

        draft_packages=Count(
            "id",
            filter=Q(status="Draft"),
        ),

        hidden_packages=Count(
            "id",
            filter=Q(status="Hidden"),
        ),
    )


    # =====================================
    # BOOKING STATISTICS
    # =====================================

    booking_stats = bookings.aggregate(

        total_bookings=Count("id"),

        pending_bookings=Count(
            "id",
            filter=Q(status="Pending"),
        ),

        approved_bookings=Count(
            "id",
            filter=Q(status="Approved"),
        ),

        rejected_bookings=Count(
            "id",
            filter=Q(status="Rejected"),
        ),

        completed_bookings=Count(
            "id",
            filter=Q(status="Completed"),
        ),

        cancelled_bookings=Count(
            "id",
            filter=Q(status="Cancelled"),
        ),
    )


    # =====================================
    # CREATE PDF RESPONSE
    # =====================================

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="company_report.pdf"'


    # =====================================
    # CREATE PDF DOCUMENT
    # =====================================

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=30,
        bottomMargin=30,
    )


    elements = []

    styles = getSampleStyleSheet()


    # =====================================
    # CUSTOM STYLES
    # =====================================

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=15,
        spaceAfter=10,
    )

    normal_style = styles["Normal"]
    table_text_style = ParagraphStyle(
        "TableText",
        parent=styles["Normal"],
        fontSize=6.5,
        leading=8,
    )


    # =====================================
    # REPORT TITLE
    # =====================================

    elements.append(
        Paragraph(
            "Trek Sathi - Company Report",
            title_style,
        )
    )


    # =====================================
    # COMPANY INFORMATION
    # =====================================

    elements.append(
        Paragraph(
            f"<b>Company:</b> {company.company_name}",
            normal_style,
        )
    )

    elements.append(
        Paragraph(
            f"<b>Report Generated:</b> "
            f"{timezone.localtime().strftime('%d %B %Y, %I:%M %p')}",
            normal_style,
        )
    )

    elements.append(
        Spacer(1, 20)
    )


    # =====================================
    # PACKAGE STATISTICS
    # =====================================

    elements.append(
        Paragraph(
            "Package Statistics",
            heading_style,
        )
    )


    package_stats_data = [

        ["Statistic", "Count"],

        [
            "Total Packages",
            package_stats["total_packages"] or 0,
        ],

        [
            "Published Packages",
            package_stats["published_packages"] or 0,
        ],

        [
            "Draft Packages",
            package_stats["draft_packages"] or 0,
        ],

        [
            "Hidden Packages",
            package_stats["hidden_packages"] or 0,
        ],
    ]


    package_stats_table = Table(
        package_stats_data,
        colWidths=[
            3.5 * inch,
            2 * inch,
        ],
    )

    package_stats_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkgreen,
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey,
            ),

            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER",
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                8,
            ),

        ])
    )

    elements.append(
        package_stats_table
    )


    elements.append(
        Spacer(1, 20)
    )


    # =====================================
    # BOOKING STATISTICS
    # =====================================

    elements.append(
        Paragraph(
            "Booking Statistics",
            heading_style,
        )
    )


    booking_stats_data = [

        ["Statistic", "Count"],

        [
            "Total Bookings",
            booking_stats["total_bookings"] or 0,
        ],

        [
            "Pending",
            booking_stats["pending_bookings"] or 0,
        ],

        [
            "Approved",
            booking_stats["approved_bookings"] or 0,
        ],

        [
            "Rejected",
            booking_stats["rejected_bookings"] or 0,
        ],

        [
            "Completed",
            booking_stats["completed_bookings"] or 0,
        ],

        [
            "Cancelled",
            booking_stats["cancelled_bookings"] or 0,
        ],
    ]


    booking_stats_table = Table(
        booking_stats_data,
        colWidths=[
            3.5 * inch,
            2 * inch,
        ],
    )


    booking_stats_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkgreen,
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey,
            ),

            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER",
            ),

        ])
    )


    elements.append(
        booking_stats_table
    )


    elements.append(
        Spacer(1, 20)
    )


    # =====================================
    # PACKAGE DETAILS TABLE
    # =====================================

    elements.append(
        Paragraph(
            "Package Details",
            heading_style,
        )
    )


    package_data = [

        [
            "Package",
            "Trek",
            "Start",
            "End",
            "Price",
            "Max People",
            "Status",
        ]
    ]

    for package in packages:

        package_data.append([

            Paragraph(
                str(package.title),
                table_text_style,
            ),

            Paragraph(
                str(package.trek.name),
                table_text_style,
            ),

            Paragraph(
                package.start_date.strftime("%d %b %Y"),
                table_text_style,
            ),

            Paragraph(
                package.end_date.strftime("%d %b %Y"),
                table_text_style,
            ),

            Paragraph(
                f"NPR {package.price_per_person}",
                table_text_style,
            ),

            Paragraph(
                str(package.max_participants),
                table_text_style,
            ),

            Paragraph(
                package.status,
                table_text_style,
            ),

        ])

        if packages.count() == 0:

            package_data.append(
                [
                    "No packages found",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )


    package_table = Table(
        package_data,
        repeatRows=1,
        colWidths=[
            1.25 * inch,  # Package
            1.05 * inch,  # Trek
            0.75 * inch,  # Start
            0.75 * inch,  # End
            0.85 * inch,  # Price
            0.65 * inch,  # Max People
            0.70 * inch,  # Status
        ],
    )


    package_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkgreen,
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.grey,
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                7,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),

            (
                "BOTTOMPADDING",
                (0, 1),
                (-1, -1),
                5,
            ),

        ])
    )


    elements.append(
        package_table
    )


    elements.append(
        Spacer(1, 20)
    )


    # =====================================
    # RECENT BOOKING DETAILS
    # =====================================

    elements.append(
        Paragraph(
            "Recent Booking Details",
            heading_style,
        )
    )


    booking_data = [

        [
            "ID",
            "Package",
            "Trekker",
            "People",
            "Total Price",
            "Status",
            "Booking Date",
        ]
    ]


    # Limit to latest 10 bookings
    recent_bookings = bookings[:10]

    for booking in recent_bookings:


        trekker_name = (
            booking.trekker.get_full_name()
            or booking.trekker.username
        )


        booking_data.append([
        
            Paragraph(
                str(booking.id),
                table_text_style,
            ),

            Paragraph(
                str(booking.package.title),
                table_text_style,
            ),

            Paragraph(
                str(trekker_name),
                table_text_style,
            ),

            Paragraph(
                str(booking.number_of_people),
                table_text_style,
            ),

            Paragraph(
                f"NPR {booking.total_price}",
                table_text_style,
            ),

            Paragraph(
                str(booking.status),
                table_text_style,
            ),

            Paragraph(
                booking.booking_date.strftime(
                    "%d %b %Y"
                ),
                table_text_style,
            ),

        ])


    if not recent_bookings:

        booking_data.append(
            [
                "No bookings found",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )


    booking_table = Table(
        booking_data,
        repeatRows=1,
        colWidths=[
            0.35 * inch,  # ID
            1.15 * inch,  # Package
            1.00 * inch,  # Trekker
            0.50 * inch,  # People
            0.75 * inch,  # Total Price
            0.70 * inch,  # Status
            0.85 * inch,  # Booking Date
        ],
    )


    booking_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkgreen,
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.grey,
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, 0),
                "MIDDLE",
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),

        ])
    )


    elements.append(
        booking_table
    )


    # =====================================
    # BUILD PDF
    # =====================================

    document.build(elements)


    return response

