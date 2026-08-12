from django.db import models
from django.contrib.auth.models import User

from bookings.models import Booking
from packages.models import Package


class Review(models.Model):

    RATING_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    trekker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review",
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.package.title} - {self.rating}★"
