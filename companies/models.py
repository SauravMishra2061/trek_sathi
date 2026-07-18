from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company"
    )

    company_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    registration_number = models.CharField(max_length=100, unique=True)

    address = models.TextField(blank=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name