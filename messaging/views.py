from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from .forms import MessageForm


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
def conversation_detail(request, pk):

    conversation = get_object_or_404(
        Conversation,
        pk=pk
    )

    if request.method == "POST":

        form = MessageForm(request.POST)

        if form.is_valid():

            message = form.save(commit=False)

            message.conversation = conversation

            message.sender = request.user

            message.save()

            return redirect(
                "conversation_detail",
                pk=conversation.pk
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