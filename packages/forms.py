from django import forms
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
            }),

            "trek": forms.Select(attrs={
                "class": "form-control",
            }),

            "price_per_person": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Price per person",
            }),

            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Duration (Days)",
            }),

            "max_participants": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Maximum Participants",
            }),

            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),

            "end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),

            "difficulty": forms.Select(attrs={
                "class": "form-control",
            }),

            "max_altitude": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Altitude (m)",
            }),

            "inclusions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
            }),

            "exclusions": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
            }),

            "itinerary": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
            }),

            "cover_image": forms.ClearableFileInput(attrs={
            "class": "form-control",
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["trek"].queryset = Trek.objects.filter(
        is_active=True,
        region__is_active=True
        ).order_by("name")

