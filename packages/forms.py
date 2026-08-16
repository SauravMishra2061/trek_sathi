from django import forms
from datetime import date

from .models import Package
from treks.models import Trek


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package

        exclude = [
            "company",
            "status",
            "created_at",
            "updated_at",
            "is_featured",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Package Title",
                "maxlength": "200",
            }),

            "trek": forms.Select(attrs={
                "class": "form-control",
            }),

            "price_per_person": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Price per person",
                "min": "1",
                "step": "0.01",
            }),

            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Duration (Days)",
                "min": "1",
            }),

            "max_participants": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Maximum Participants",
                "min": "1",
            }),

            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "min": date.today().isoformat(),
            }),

            "end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "min": date.today().isoformat(),
            }),

            "difficulty": forms.Select(attrs={
                "class": "form-control",
            }),

            "max_altitude": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Altitude (m)",
                "min": "1",
            }),

            "inclusions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "What is included in this package?",
            }),

            "exclusions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "What is not included?",
            }),

            "itinerary": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Describe the day-by-day itinerary.",
            }),

            "cover_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".jpg,.jpeg,.png",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["trek"].queryset = Trek.objects.filter(
            is_active=True,
            region__is_active=True
        ).order_by("name")

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()

        if not title:
            raise forms.ValidationError(
                "Package title is required."
            )

        if len(title) < 3:
            raise forms.ValidationError(
                "Package title must be at least 3 characters long."
            )

        return title

    def clean_price_per_person(self):
        price = self.cleaned_data.get("price_per_person")

        if price is None:
            raise forms.ValidationError(
                "Price per person is required."
            )

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than 0."
            )

        return price

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")

        if duration is None:
            raise forms.ValidationError(
                "Duration is required."
            )

        if duration <= 0:
            raise forms.ValidationError(
                "Duration must be at least 1 day."
            )

        return duration

    def clean_max_participants(self):
        participants = self.cleaned_data.get("max_participants")

        if participants is None:
            raise forms.ValidationError(
                "Maximum participants is required."
            )

        if participants <= 0:
            raise forms.ValidationError(
                "Maximum participants must be at least 1."
            )

        return participants

    def clean_max_altitude(self):
        altitude = self.cleaned_data.get("max_altitude")

        if altitude is None:
            raise forms.ValidationError(
                "Maximum altitude is required."
            )

        if altitude <= 0:
            raise forms.ValidationError(
                "Maximum altitude must be greater than 0."
            )

        return altitude

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")

        if not start_date:
            raise forms.ValidationError(
                "Start date is required."
            )

        if start_date < date.today():
            raise forms.ValidationError(
                "Start date cannot be in the past."
            )

        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get("end_date")

        if not end_date:
            raise forms.ValidationError(
                "End date is required."
            )

        return end_date

    def clean_cover_image(self):
        image = self.cleaned_data.get("cover_image")

        if not image:
            return image

        max_size = 5 * 1024 * 1024  # 5 MB

        if image.size > max_size:
            raise forms.ValidationError(
                "Cover image cannot exceed 5 MB."
            )

        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
        ]

        filename = image.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions
        ):
            raise forms.ValidationError(
                "Only JPG, JPEG, and PNG images are allowed."
            )

        return image

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:

            if end_date < start_date:
                self.add_error(
                    "end_date",
                    "End date cannot be before the start date."
                )

        return cleaned_data