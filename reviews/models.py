from django.db import models
from django.contrib.auth.models import User
from packages.models import Package


class Review(models.Model):

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    trekker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.package.title} - {self.rating}★"