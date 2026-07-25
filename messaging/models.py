from django.db import models
from django.contrib.auth.models import User
from packages.models import Package
from companies.models import Company


class Conversation(models.Model):

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
    ]

    trekker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    subject = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.package.title})"


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username}"