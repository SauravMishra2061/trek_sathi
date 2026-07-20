from django import forms
from .models import Trek
from regions.models import Region


class TrekForm(forms.ModelForm):

    class Meta:
        model = Trek

        fields = [
            "region",
            "name",
            "description",
            "altitude",
            "difficulty",
            "image",
            "is_active",
        ]

        widgets = {

            "region": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Trek Name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Trek Description"
                }
            ),

            "altitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Maximum Altitude (m)"
                }
            ),

            "difficulty": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["region"].queryset = Region.objects.filter(
            is_active=True
        ).order_by("name")

    def clean_region(self):
        region = self.cleaned_data["region"]

        if not region.is_active:
            raise forms.ValidationError(
                "You cannot create a trek under an inactive region."
            )

        return region