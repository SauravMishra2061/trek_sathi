from django.shortcuts import render 
from django.contrib.auth.decorators import login_required

from .models import Trek

from .forms import TrekForm
from django.shortcuts import get_object_or_404, redirect
@login_required
def trek_list(request):

    treks = Trek.objects.all()

    return render(
        request,
        "treks/trek_list.html",
        {
            "treks": treks
        }
    )


@login_required
def add_trek(request):

    if request.method == "POST":

        form = TrekForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("trek_list")

    else:

        form = TrekForm()

    return render(
        request,
        "treks/trek_form.html",
        {
            "form": form,
            "title": "Add Trek"
        }
    )


@login_required
def edit_trek(request, pk):

    trek = get_object_or_404(
        Trek,
        pk=pk
    )

    if request.method == "POST":

        form = TrekForm(
            request.POST,
            request.FILES,
            instance=trek
        )

        if form.is_valid():

            form.save()

            return redirect("trek_list")

    else:

        form = TrekForm(
            instance=trek
        )

    return render(

        request,

        "treks/trek_form.html",

        {

            "form":form,

            "title":"Edit Trek"

        }

    )

@login_required
def delete_trek(request, pk):

    trek = get_object_or_404(Trek, pk=pk)

    if request.method == "POST":
        trek.delete()
        return redirect("trek_list")

    return render(
        request,
        "treks/trek_confirm_delete.html",
        {
            "trek": trek
        }
    )