from django.shortcuts import render 
from django.contrib.auth.decorators import login_required

from .models import Region

from .forms import RegionForm
from django.shortcuts import get_object_or_404, redirect
@login_required
def region_list(request):

    regions = Region.objects.all()

    return render(
        request,
        "regions/region_list.html",
        {
            "regions": regions
        }
    )


@login_required
def add_region(request):

    if request.method == "POST":

        form = RegionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("region_list")

    else:

        form = RegionForm()

    return render(
        request,
        "regions/region_form.html",
        {
            "form": form,
            "title": "Add Region"
        }
    )


@login_required
def edit_region(request, pk):

    region = get_object_or_404(
        Region,
        pk=pk
    )

    if request.method == "POST":

        form = RegionForm(
            request.POST,
            request.FILES,
            instance=region
        )

        if form.is_valid():

            form.save()

            return redirect("region_list")

    else:

        form = RegionForm(
            instance=region
        )

    return render(

        request,

        "regions/region_form.html",

        {

            "form":form,

            "title":"Edit Region"

        }

    )

@login_required
def delete_region(request, pk):

    region = get_object_or_404(Region, pk=pk)

    if request.method == "POST":
        region.delete()
        return redirect("region_list")

    return render(
        request,
        "regions/region_confirm_delete.html",
        {
            "region": region
        }
    )