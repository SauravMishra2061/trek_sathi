from django.db import models
from django.contrib.auth.models import User
from packages.models import Package


class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    trekker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    number_of_people = models.PositiveIntegerField(default=1)

    emergency_contact = models.CharField(max_length=20)

    special_request = models.TextField(blank=True)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trekker.username} - {self.package.title}"