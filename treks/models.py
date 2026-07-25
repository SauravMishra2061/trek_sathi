from django.db import models
from regions.models import Region


class Trek(models.Model):

    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Moderate", "Moderate"),
        ("Hard", "Hard"),
        ("Extreme", "Extreme"),
    ]

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="treks"
    )

    name = models.CharField(max_length=150)

    description = models.TextField()

    altitude = models.PositiveIntegerField(
        help_text="Maximum altitude in meters"
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES
    )

    image = models.ImageField(
        upload_to="treks/"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
