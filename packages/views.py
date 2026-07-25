from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from packages.models import Package
from .forms import PackageForm
from .models import Package
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import PackageImage

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

    if request.method == "POST":

        form = PackageForm(request.POST, request.FILES)

        if form.is_valid():

            package = form.save(commit=False)

            package.company = request.user.company

            if "publish" in request.POST:
                package.status = "Published"
            else:
                package.status = "Draft"

            package.save()

            for image in request.FILES.getlist("images"):

                PackageImage.objects.create(
                    package=package,
                    image=image
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




@login_required
def package_detail(request, pk):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    package = get_object_or_404(
        Package,
        pk=pk,
        company=request.user.company
    )

    return render(
        request,
        "packages/package_detail.html",
        {
            "package": package,
        },
    )


@login_required
def edit_package(request, pk):

    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    package = get_object_or_404(
        Package,
        pk=pk,
        company=request.user.company
    )

    if request.method == "POST":

        form = PackageForm(request.POST,  request.FILES, instance=package)

        if form.is_valid():

            package = form.save(commit=False)

            package.company = request.user.company

            if "publish" in request.POST:
                package.status = "Published"
                messages.success(request, "Package updated successfully.")
            else:
                package.status = "Draft"
                messages.info(request, "Draft updated successfully.")

            package.save()

            return redirect("package_detail", pk=package.pk)

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

    package = get_object_or_404(
        Package,
        pk=pk,
        company=request.user.company
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