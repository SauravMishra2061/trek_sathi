from django.db import models
from companies.models import Company
from treks.models import Trek


class Package(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
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

    title = models.CharField(max_length=200)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in days"
    )

    available_slots = models.PositiveIntegerField()

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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"
    
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