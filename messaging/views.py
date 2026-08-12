from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from packages.models import Package
from .models import Conversation, Message
from .forms import MessageForm, EnquiryForm


@login_required
def company_inbox(request):
    if not hasattr(request.user, "company"):
        return redirect("trekker_dashboard")

    conversations = Conversation.objects.filter(
        company=request.user.company
    ).order_by("-created_at")

    return render(
        request,
        "messaging/company_inbox.html",
        {
            "conversations": conversations,
        },
    )


@login_required
def my_conversations(request):

    conversations = (
        Conversation.objects.filter(
            trekker=request.user
        )
        .select_related(
            "company",
            "package"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "messaging/my_conversations.html",
        {
            "conversations": conversations,
        },
    )

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation,
        pk=pk,
    )

    # Permission check
    if hasattr(request.user, "company"):
        if conversation.company != request.user.company:
            return redirect("company_inbox")
    else:
        if conversation.trekker != request.user:
            return redirect("my_conversations")

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()

            return redirect(
                "conversation_detail",
                pk=conversation.pk,
            )
    else:
        form = MessageForm()

    return render(
        request,
        "messaging/conversation_detail.html",
        {
            "conversation": conversation,
            "form": form,
        },
    )


@login_required
def start_enquiry(request, package_id):
    package = get_object_or_404(
        Package,
        pk=package_id,
    )

    # Reuse existing open conversation for this package
    conversation = Conversation.objects.filter(
        trekker=request.user,
        package=package,
        status="Open",
    ).first()

    if conversation:
        return redirect(
            "conversation_detail",
            pk=conversation.pk,
        )

    if request.method == "POST":
        form = EnquiryForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(
                trekker=request.user,
                company=package.company,
                package=package,
                subject=form.cleaned_data["subject"],
            )

            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                message=form.cleaned_data["message"],
            )

            return redirect(
                "conversation_detail",
                pk=conversation.pk,
            )

    else:
        form = EnquiryForm(
            initial={
                "subject": f"Enquiry about {package.title}",
            }
        )

    return render(
        request,
        "messaging/start_enquiry.html",
        {
            "package": package,
            "form": form,
        },
    )