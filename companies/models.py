from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Suspended", "Suspended"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company"
    )

    company_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True,null=True)

    registration_number = models.CharField(
        max_length=100,
        unique=True
    )

    address = models.TextField(blank=True)

    description = models.TextField(blank=True)

    admin_feedback = models.TextField(
    blank=True,
    null=True,
    help_text="Admin remarks for approval, rejection or suspension."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    registration_document = models.FileField(
        upload_to="company_documents/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
    
admin_feedback = models.TextField(
    blank=True,
    null=True,
    help_text="Admin remarks for approval, rejection or suspension."
)