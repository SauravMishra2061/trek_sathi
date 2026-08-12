from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PackageForm
from .models import Package, PackageImage, SavedPackage
from bookings.models import Booking


@login_required
def package_list(request):
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company
    packages = Package.objects.filter(company=company)

    return render(
        request,
        "packages/package_list.html",
        {
            "packages": packages,
            "has_packages": packages.exists(),
        },
    )


@login_required
def add_package(request):
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    if company.status != "Approved":
        messages.error(
            request,
            "Your company must be approved before you can create packages."
        )
        return redirect("company_dashboard")

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)

        if form.is_valid():
            package = form.save(commit=False)
            package.company = company

            if "publish" in request.POST:
                package.status = "Published"
            else:
                package.status = "Draft"

            package.save()

            for image in request.FILES.getlist("images"):
                PackageImage.objects.create(
                    package=package,
                    image=image,
                )

            messages.success(
                request,
                "Package created successfully."
            )

            return redirect("package_list")

    else:
        form = PackageForm()

    return render(
        request,
        "packages/add_package.html",
        {
            "form": form,
        },
    )

def package_detail(request, pk):

    package = get_object_or_404(
        Package.objects.select_related(
            "company",
            "trek",
            "trek__region",
        ),
        pk=pk,
        status="Published",
    )

    reviews = package.reviews.select_related(
        "trekker"
    ).order_by("-created_at")

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    user_booking = None
    is_saved = False

    if request.user.is_authenticated and not hasattr(request.user, "company"):

        user_booking = (
            Booking.objects.filter(
                trekker=request.user,
                package=package,
            )
            .order_by("-booking_date")
            .first()
        )

        is_saved = SavedPackage.objects.filter(
            trekker=request.user,
            package=package,
        ).exists()

    return render(
        request,
        "packages/package_detail.html",
        {
            "package": package,
            "reviews": reviews,
            "average_rating": average_rating,
            "user_booking": user_booking,
            "is_saved": is_saved,
        },
    )
@login_required
def company_package_detail(request, pk):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    package = get_object_or_404(
        Package.objects.select_related(
            "company",
            "trek",
            "trek__region",
        ),
        pk=pk,
        company=request.user.company,
    )

    reviews = package.reviews.select_related(
        "trekker"
    ).order_by("-created_at")

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    return render(
        request,
        "packages/company_package_detail.html",
        {
            "package": package,
            "reviews": reviews,
            "average_rating": average_rating,
        },
    )

@login_required
def edit_package(request, pk):
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    if company.status != "Approved":
        messages.error(
            request,
            "Your company must be approved before you can edit packages."
        )
        return redirect("company_dashboard")

    package = get_object_or_404(
        Package,
        pk=pk,
        company=company,
    )

    if request.method == "POST":
        form = PackageForm(
            request.POST,
            request.FILES,
            instance=package,
        )

        if form.is_valid():
            package = form.save(commit=False)
            package.company = company

            if "publish" in request.POST:
                package.status = "Published"
                messages.success(
                    request,
                    "Package updated successfully."
                )
            else:
                package.status = "Draft"
                messages.info(
                    request,
                    "Draft updated successfully."
                )

            package.save()

            return redirect(
                "company_package_detail",
                pk=package.pk,
            )

    else:
        form = PackageForm(instance=package)

    return render(
        request,
        "packages/edit_package.html",
        {
            "form": form,
            "package": package,
        },
    )
@login_required
def delete_package(request, pk):
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    if company.status != "Approved":
        messages.error(
            request,
            "Your company must be approved before you can delete packages."
        )
        return redirect("company_dashboard")

    package = get_object_or_404(
        Package,
        pk=pk,
        company=company,
    )

    if request.method == "POST":
        package.delete()

        messages.success(
            request,
            "Package deleted successfully."
        )

        return redirect("package_list")

    return render(
        request,
        "packages/delete_package.html",
        {
            "package": package,
        },
    )

@login_required
def save_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)

    saved = SavedPackage.objects.filter(
        trekker=request.user,
        package=package,
    )

    if saved.exists():
        saved.delete()
    else:
        SavedPackage.objects.create(
            trekker=request.user,
            package=package,
        )

    return redirect(request.META.get("HTTP_REFERER", "home"))

@login_required
def saved_packages(request):

    if hasattr(request.user, "company"):
        return redirect("company_dashboard")

    saved_packages = (
        SavedPackage.objects.filter(trekker=request.user)
        .select_related(
            "package",
            "package__company",
            "package__trek",
        )
        .order_by("-saved_at")
    )

    return render(
        request,
        "packages/saved_packages.html",
        {
            "saved_packages": saved_packages,
        },
    )