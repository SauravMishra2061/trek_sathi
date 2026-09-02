from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User

from companies.models import Company
from treks.models import Trek


class Package(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Published", "Published"),
        ("Hidden", "Hidden"),
    ]

    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Moderate", "Moderate"),
        ("Hard", "Hard"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    trek = models.ForeignKey(
        Trek,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    # =====================================
    # MAIN COVER IMAGE
    # =====================================

    cover_image = models.ImageField(
        upload_to="package_cover/",
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=200
    )

    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in days"
    )

    max_participants = models.PositiveIntegerField()

    is_featured = models.BooleanField(
        default=False
    )

    start_date = models.DateField()

    end_date = models.DateField()

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES
    )

    max_altitude = models.PositiveIntegerField(
        help_text="Altitude in meters"
    )

    inclusions = models.TextField()

    exclusions = models.TextField()

    itinerary = models.TextField()

    # =====================================
    # TREKKING ROUTE
    # =====================================

    route_points = models.JSONField(
        default=list,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================
    # DISPLAY PACKAGE
    # =====================================

    def __str__(self):

        return (
            f"{self.title} - "
            f"{self.company.company_name}"
        )

    # =====================================
    # CHECK IF PACKAGE IS EXPIRED
    # =====================================

    @property
    def is_expired(self):

        return (
            self.end_date
            < timezone.localdate()
        )

    # =====================================
    # CHECK IF PACKAGE HAS STARTED
    # =====================================

    @property
    def has_started(self):

        return (
            self.start_date
            <= timezone.localdate()
        )

    # =====================================
    # OCCUPIED SLOTS
    # =====================================

    @property
    def occupied_slots(self):

        total = (
            self.bookings.filter(
                status__in=[
                    "Pending",
                    "Approved",
                    "Completed",
                ]
            )
            .aggregate(
                total=Sum(
                    "number_of_people"
                )
            )
            .get("total")
            or 0
        )

        return total

    # =====================================
    # REMAINING SLOTS
    # =====================================

    @property
    def remaining_slots(self):

        remaining = (
            self.max_participants
            - self.occupied_slots
        )

        return max(
            0,
            remaining
        )

    # =====================================
    # CHECK IF PACKAGE IS FULL
    # =====================================

    @property
    def is_full(self):

        return (
            self.remaining_slots <= 0
        )

    # =====================================
    # CHECK IF PACKAGE CAN BE BOOKED
    # =====================================

    @property
    def is_available_for_booking(self):

        return (
            self.status == "Published"
            and not self.is_expired
            and not self.has_started
            and self.remaining_slots > 0
        )


# =====================================
# PACKAGE GALLERY IMAGES
# =====================================

class PackageImage(models.Model):

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="package_images/"
    )

    def __str__(self):

        return self.package.title


# =====================================
# SAVED PACKAGES
# =====================================

class SavedPackage(models.Model):

    trekker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_packages"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "trekker",
            "package"
        )

    def __str__(self):

        return (
            f"{self.trekker.username} - "
            f"{self.package.title}"
        )