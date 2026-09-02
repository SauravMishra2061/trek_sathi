from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from companies.models import Company, TrekRequest
from django.shortcuts import get_object_or_404
from adminpanel.forms import TrekRequestReviewForm
from treks.models import Trek
from django.contrib import messages
from .forms import TrekRequestReviewForm
from django.contrib.auth import get_user_model
from regions.models import Region
from packages.models import Package
from bookings.models import Booking
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    total_regions = Region.objects.count()

    total_treks = Trek.objects.count()

    total_companies = Company.objects.count()

    total_users = User.objects.filter(
        is_staff=False
    ).count()

    total_packages = Package.objects.count()

    total_bookings = Booking.objects.count()

    pending_companies = Company.objects.filter(
        status="Pending"
    ).count()

    approved_companies = Company.objects.filter(
        status="Approved"
    ).count()

    context = {
        "total_regions": total_regions,
        "total_treks": total_treks,
        "total_companies": total_companies,
        "total_users": total_users,

        "total_packages": total_packages,
        "total_bookings": total_bookings,

        "pending_companies": pending_companies,
        "approved_companies": approved_companies,
    }

    return render(
        request,
        "adminpanel/admin_dashboard.html",
        context
    )


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
def review_company(request, pk):

    if not request.user.is_staff:
        return redirect("trekker_dashboard")

    company = get_object_or_404(
        Company.objects.select_related("user"),
        pk=pk,
    )

    if request.method == "POST":

        action = request.POST.get("action")
        feedback = request.POST.get(
            "admin_feedback",
            ""
        ).strip()

        if action == "approve":

            company.status = "Approved"
            company.admin_feedback = feedback
            company.approval_message_seen = False
            company.save()

            messages.success(
                request,
                f"{company.company_name} has been approved."
            )

        elif action == "reject":

            company.status = "Rejected"
            company.admin_feedback = feedback
            company.approval_message_seen = False
            company.save()

            messages.success(
                request,
                f"{company.company_name} has been rejected."
            )

        elif action == "suspend":

            company.status = "Suspended"
            company.admin_feedback = feedback
            company.approval_message_seen = False
            company.save()

            messages.success(
                request,
                f"{company.company_name} has been suspended."
            )

        return redirect("admin_companies")

    return render(
        request,
        "adminpanel/review_company.html",
        {
            "company": company,
            "document": company.registration_document,
        },
    )


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

   # requests = requests.order_by("-created_at")

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

@login_required
def generate_admin_report(request):


# =====================================
# SECURITY
# =====================================

    if not request.user.is_staff:
        return redirect("trekker_dashboard")


# =====================================
# RESPONSE
# =====================================

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="admin_report.pdf"'
    )


# =====================================
# PDF DOCUMENT
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


# =====================================
# STYLES
# =====================================

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    heading_style = styles["Heading2"]

    normal_style = styles["Normal"]


    table_text_style = ParagraphStyle(
        "TableText",
        parent=styles["Normal"],
        fontSize=6.5,
        leading=8,
    )


# =====================================
# REPORT TITLE
#=====================================

    elements.append(
        Paragraph(
            "Trek Sathi Platform Report",
            title_style,
        )
    )


    elements.append(
        Spacer(
            1,
            10,
        )
    )


    elements.append(
        Paragraph(
            f"Report Generated: "
            f"{timezone.localtime().strftime('%d %B %Y, %I:%M %p')}",
            normal_style,
        )
    )


    elements.append(
        Paragraph(
            f"Generated By: "
            f"{request.user.username}",
            normal_style,
        )
    )


    elements.append(
        Spacer(
            1,
            20,
        )
    )


    # =====================================
    # PLATFORM STATISTICS
    # =====================================

    elements.append(
        Paragraph(
            "Platform Overview",
            heading_style,
        )
    )


    platform_data = [

        [
            "Regions",
            "Treks",
            "Companies",
            "Users",
        ],

        [
            str(
                Region.objects.count()
            ),

            str(
                Trek.objects.count()
            ),

            str(
                Company.objects.count()
            ),

            str(
                User.objects.filter(
                    is_staff=False
                ).count()
            ),
        ],
    ]


    platform_table = Table(
        platform_data,
        colWidths=[
            1.25 * inch,
            1.25 * inch,
            1.25 * inch,
            1.25 * inch,
        ],
    )


    platform_table.setStyle(
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
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER",
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
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

        ])
    )


    elements.append(
        platform_table
    )


    elements.append(
        Spacer(
            1,
            20,
        )
    )


    # =====================================
    # COMPANY STATISTICS
    # =====================================

    elements.append(
        Paragraph(
            "Company Statistics",
            heading_style,
        )
    )


    company_stats_data = [

        [
            "Total",
            "Pending",
            "Approved",
            "Rejected",
            "Suspended",
        ],

        [

            str(
                Company.objects.count()
            ),

            str(
                Company.objects.filter(
                    status="Pending"
                ).count()
            ),

            str(
                Company.objects.filter(
                    status="Approved"
                ).count()
            ),

            str(
                Company.objects.filter(
                    status="Rejected"
                ).count()
            ),

            str(
                Company.objects.filter(
                    status="Suspended"
                ).count()
            ),

        ],
    ]


    company_stats_table = Table(
        company_stats_data,
        colWidths=[
            1.05 * inch,
            1.05 * inch,
            1.05 * inch,
            1.05 * inch,
            1.05 * inch,
        ],
    )


    company_stats_table.setStyle(
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
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER",
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
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

        ])
    )


    elements.append(
        company_stats_table
    )


    elements.append(
        Spacer(
            1,
            20,
        )
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

        [
            "Total",
            "Published",
            "Draft",
            "Hidden",
        ],

        [

            str(
                Package.objects.count()
            ),

            str(
                Package.objects.filter(
                    status="Published"
                ).count()
            ),

            str(
                Package.objects.filter(
                    status="Draft"
                ).count()
            ),

            str(
                Package.objects.filter(
                    status="Hidden"
                ).count()
            ),

        ],
    ]


    package_stats_table = Table(
        package_stats_data,
        colWidths=[
            1.25 * inch,
            1.25 * inch,
            1.25 * inch,
            1.25 * inch,
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
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER",
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
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

        ])
    )


    elements.append(
        package_stats_table
    )


    elements.append(
        Spacer(
            1,
            20,
        )
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

        [
            "Total",
            "Pending",
            "Approved",
            "Rejected",
            "Completed",
            "Cancelled",
        ],

        [

            str(
                Booking.objects.count()
            ),

            str(
                Booking.objects.filter(
                    status="Pending"
                ).count()
            ),

            str(
                Booking.objects.filter(
                    status="Approved"
                ).count()
            ),

            str(
                Booking.objects.filter(
                    status="Rejected"
                ).count()
            ),

            str(
                Booking.objects.filter(
                    status="Completed"
                ).count()
            ),

            str(
                Booking.objects.filter(
                    status="Cancelled"
                ).count()
            ),

        ],
    ]


    booking_stats_table = Table(
        booking_stats_data,
        colWidths=[
            0.85 * inch,
            0.85 * inch,
            0.85 * inch,
            0.85 * inch,
            0.85 * inch,
            0.85 * inch,
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
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER",
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
                0.5,
                colors.grey,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),

        ])
    )


    elements.append(
        booking_stats_table
    )


    elements.append(
        Spacer(
            1,
            20,
        )
    )


# =====================================
# RECENT COMPANIES
# =====================================

    elements.append(
        Paragraph(
            "Recent Companies",
            heading_style,
        )
    )


    recent_companies = (
        Company.objects
        .select_related("user")
        .order_by("-id")[:10]
    )


    company_data = [

        [
            "Company",
            "Owner",
            "Status",
        ]
    ]


    for company in recent_companies:

        owner_name = (
            company.user.get_full_name()
            or company.user.username
        )


        company_data.append([

            Paragraph(
                str(company.company_name),
                table_text_style,
            ),

            Paragraph(
                str(owner_name),
                table_text_style,
            ),

            Paragraph(
                str(company.status),
                table_text_style,
            ),

        ])


    company_table = Table(
        company_data,
        repeatRows=1,
        colWidths=[
            2.2 * inch,
            2.0 * inch,
            1.3 * inch,
        ],
    )


    company_table.setStyle(
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
        company_table
    )


    elements.append(
        Spacer(
            1,
            20,
        )
    )


    # =====================================
    # PACKAGE DETAILS
    # =====================================

    elements.append(
        Paragraph(
            "Package Details",
            heading_style,
        )
    )


    packages = (
        Package.objects
        .select_related(
            "company",
            "trek",
        )
        .order_by("-created_at")
    )


    package_data = [

        [
            "Package",
            "Company",
            "Trek",
            "Start",
            "End",
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
                str(
                    package.company.company_name
                ),
                table_text_style,
            ),

            Paragraph(
                str(package.trek.name),
                table_text_style,
            ),

            Paragraph(
                package.start_date.strftime(
                    "%d %b %Y"
                ),
                table_text_style,
            ),

            Paragraph(
                package.end_date.strftime(
                    "%d %b %Y"
                ),
                table_text_style,
            ),

            Paragraph(
                str(package.status),
                table_text_style,
            ),

        ])


    package_table = Table(
        package_data,
        repeatRows=1,
        colWidths=[
            1.25 * inch,
            1.05 * inch,
            1.05 * inch,
            0.75 * inch,
            0.75 * inch,
            0.70 * inch,
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
                6.5,
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
        package_table
    )


    elements.append(
        Spacer(
            1,
            20,
        )
    )


    # =====================================
    # RECENT BOOKINGS
    # =====================================

    elements.append(
        Paragraph(
            "Recent Bookings",
            heading_style,
        )
    )


    recent_bookings = (
        Booking.objects
        .select_related(
            "package",
            "trekker",
        )
        .order_by("-booking_date")[:15]
    )


    booking_data = [

        [
            "ID",
            "Package",
            "Trekker",
            "People",
            "Price",
            "Status",
            "Date",
        ]
    ]


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


    booking_table = Table(
        booking_data,
        repeatRows=1,
        colWidths=[
            0.35 * inch,
            1.15 * inch,
            1.00 * inch,
            0.50 * inch,
            0.75 * inch,
            0.70 * inch,
            0.85 * inch,
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
                6.5,
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

    document.build(
        elements
    )


    return response

