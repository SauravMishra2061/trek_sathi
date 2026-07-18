from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def trekker_dashboard(request):

    if hasattr(request.user, "company"):
        return redirect("company_dashboard")
    return render(request, "dashboard/trekker_dashboard.html")