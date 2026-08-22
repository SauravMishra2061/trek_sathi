from django.db import models
from companies.models import Company
from treks.models import Trek
from django.contrib.auth.models import User


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

    # Main Cover Image
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

    # Stores trekking route locations
    # Example:
    # [
    #   {
    #       "name": "Lukla",
    #       "displayName": "Lukla, Solukhumbu, Nepal",
    #       "latitude": 27.6869,
    #       "longitude": 86.7296
    #   }
    # ]
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

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"


# Package Gallery Images
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


# Saved Packages
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
        return f"{self.trekker.username} - {self.package.title}"