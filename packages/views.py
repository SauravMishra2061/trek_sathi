from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PackageForm
from .models import Package, PackageImage, SavedPackage
from bookings.models import Booking

import json
import requests

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def package_list(request):
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    company = request.user.company

    packages = Package.objects.filter(
        company=company
    )

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
            "Your company must be approved before you can create packages.",
        )

        return redirect(
            "company_dashboard"
        )

    if request.method == "POST":

        form = PackageForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            package = form.save(
                commit=False
            )

            package.company = company

            # =================================
            # SAVE TREKKING ROUTE
            # =================================

            route_points_data = request.POST.get(
                "route_points",
                "",
            )

            try:

                route_data = json.loads(
                    route_points_data
                )

                # ---------------------------------
                # New format
                #
                # {
                #     "points": [...],
                #     "geometry": "encoded-polyline"
                # }
                # ---------------------------------

                if isinstance(
                    route_data,
                    dict
                ):

                    if not isinstance(
                        route_data.get("points"),
                        list
                    ):

                        route_data["points"] = []

                    # Ensure geometry exists

                    if "geometry" not in route_data:

                        route_data["geometry"] = None

                    package.route_points = route_data

                # ---------------------------------
                # Old format support
                #
                # [
                #     {...},
                #     {...}
                # ]
                # ---------------------------------

                elif isinstance(
                    route_data,
                    list
                ):

                    package.route_points = {
                        "points": route_data,
                        "geometry": None,
                    }

                else:

                    package.route_points = {
                        "points": [],
                        "geometry": None,
                    }

            except (
                json.JSONDecodeError,
                TypeError,
            ):

                package.route_points = {
                    "points": [],
                    "geometry": None,
                }

            # =================================
            # PACKAGE STATUS
            # =================================

            if "publish" in request.POST:

                package.status = "Published"

            else:

                package.status = "Draft"

            package.save()

            # =================================
            # SAVE PACKAGE IMAGES
            # =================================

            for image in request.FILES.getlist(
                "images"
            ):

                PackageImage.objects.create(
                    package=package,
                    image=image,
                )

            messages.success(
                request,
                "Package created successfully.",
            )

            return redirect(
                "package_list"
            )

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
    ).order_by(
        "-created_at"
    )

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    user_booking = None

    is_saved = False

    if (
        request.user.is_authenticated
        and not hasattr(
            request.user,
            "company"
        )
    ):

        user_booking = (
            Booking.objects.filter(
                trekker=request.user,
                package=package,
            )
            .order_by(
                "-booking_date"
            )
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

    if not hasattr(
        request.user,
        "company"
    ):

        return redirect(
            "trekker_dashboard"
        )

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
    ).order_by(
        "-created_at"
    )

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

    # =================================
    # CHECK COMPANY USER
    # =================================

    if not hasattr(
        request.user,
        "company"
    ):

        return redirect(
            "trekker_dashboard"
        )

    company = request.user.company

    # =================================
    # CHECK COMPANY APPROVAL
    # =================================

    if company.status != "Approved":

        messages.error(
            request,
            "Your company must be approved before you can edit packages.",
        )

        return redirect(
            "company_dashboard"
        )

    # =================================
    # GET PACKAGE
    # =================================

    package = get_object_or_404(
        Package,
        pk=pk,
        company=company,
    )

    # =================================
    # EDIT PACKAGE
    # =================================

    if request.method == "POST":

        form = PackageForm(
            request.POST,
            request.FILES,
            instance=package,
        )

        if form.is_valid():

            package = form.save(
                commit=False
            )

            package.company = company

            # =================================
            # SAVE TREKKING ROUTE
            # =================================

            route_points_data = request.POST.get(
                "route_points",
                "{}",
            )

            try:

                route_data = json.loads(
                    route_points_data
                )

                # =================================
                # NEW ROUTE FORMAT
                #
                # {
                #     "points": [
                #         {
                #             "name": "...",
                #             "displayName": "...",
                #             "latitude": ...,
                #             "longitude": ...
                #         }
                #     ],
                #
                #     "geometry": "encoded-polyline"
                # }
                # =================================

                if isinstance(
                    route_data,
                    dict
                ):

                    # Make sure points exists
                    # and is a list

                    if not isinstance(
                        route_data.get("points"),
                        list
                    ):

                        route_data["points"] = []

                    # Make sure geometry exists

                    if "geometry" not in route_data:

                        route_data["geometry"] = None

                    package.route_points = {
                        "points": route_data["points"],
                        "geometry": route_data["geometry"],
                    }

                # =================================
                # OLD FORMAT SUPPORT
                #
                # [
                #     {
                #         "name": "...",
                #         "latitude": ...,
                #         "longitude": ...
                #     }
                # ]
                # =================================

                elif isinstance(
                    route_data,
                    list
                ):

                    package.route_points = {
                        "points": route_data,
                        "geometry": None,
                    }

                # =================================
                # INVALID DATA
                # =================================

                else:

                    package.route_points = {
                        "points": [],
                        "geometry": None,
                    }

            except (
                json.JSONDecodeError,
                TypeError,
            ):

                package.route_points = {
                    "points": [],
                    "geometry": None,
                }

            # =================================
            # PACKAGE STATUS
            # =================================

            if "publish" in request.POST:

                package.status = "Published"

                messages.success(
                    request,
                    "Package updated successfully.",
                )

            else:

                package.status = "Draft"

                messages.info(
                    request,
                    "Draft updated successfully.",
                )

            # =================================
            # SAVE PACKAGE
            # =================================

            package.save()

            # =================================
            # REDIRECT
            # =================================

            return redirect(
                "company_package_detail",
                pk=package.pk,
            )

    # =================================
    # GET REQUEST
    # =================================

    else:

        form = PackageForm(
            instance=package
        )

    # =================================
    # RENDER EDIT PAGE
    # =================================

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

    if not hasattr(
        request.user,
        "company"
    ):

        return redirect(
            "trekker_dashboard"
        )

    company = request.user.company

    if company.status != "Approved":

        messages.error(
            request,
            "Your company must be approved before you can delete packages.",
        )

        return redirect(
            "company_dashboard"
        )

    package = get_object_or_404(
        Package,
        pk=pk,
        company=company,
    )

    if request.method == "POST":

        package.delete()

        messages.success(
            request,
            "Package deleted successfully.",
        )

        return redirect(
            "package_list"
        )

    return render(
        request,
        "packages/delete_package.html",
        {
            "package": package,
        },
    )


@login_required
def save_package(
    request,
    package_id
):

    package = get_object_or_404(
        Package,
        pk=package_id,
    )

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

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


@login_required
def saved_packages(request):

    if hasattr(
        request.user,
        "company"
    ):

        return redirect(
            "company_dashboard"
        )

    saved_packages = (
        SavedPackage.objects.filter(
            trekker=request.user
        )
        .select_related(
            "package",
            "package__company",
            "package__trek",
        )
        .order_by(
            "-saved_at"
        )
    )

    return render(
        request,
        "packages/saved_packages.html",
        {
            "saved_packages": saved_packages,
        },
    )


# =================================
# CALCULATE TREKKING ROUTE
# =================================

@require_POST
def calculate_route(request):

    try:

        data = json.loads(
            request.body
        )

        coordinates = data.get(
            "coordinates",
            [],
        )

        # ---------------------------------
        # At least two locations required
        # ---------------------------------

        if len(coordinates) < 2:

            return JsonResponse(
                {
                    "error":
                    "At least two route points are required."
                },
                status=400,
            )

        # ---------------------------------
        # OPENROUTESERVICE REQUEST
        # ---------------------------------

        response = requests.post(
            "https://api.heigit.org/openrouteservice/v2/directions/foot-walking",
            headers={
                "Authorization":
                settings.ORS_API_KEY,

                "Content-Type":
                "application/json",

                "Accept":
                "application/json",
            },
            json={
                "coordinates":
                coordinates,
            },
            timeout=30,
        )

        # ---------------------------------
        # HANDLE API ERROR
        # ---------------------------------

        if not response.ok:

            return JsonResponse(
                {
                    "error":
                    "Unable to generate route.",

                    "details":
                    response.text,
                },
                status=response.status_code,
            )

        # ---------------------------------
        # RETURN ROUTE DATA
        # ---------------------------------

        return JsonResponse(
            response.json()
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error":
                "Invalid route data."
            },
            status=400,
        )

    except requests.RequestException as error:

        return JsonResponse(
            {
                "error":
                f"Routing service error: {str(error)}"
            },
            status=500,
        )

    except Exception as error:

        return JsonResponse(
            {
                "error":
                str(error)
            },
            status=500,
        )
