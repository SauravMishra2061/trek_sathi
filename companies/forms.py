from django import forms
from .models import Company
from .models import TrekRequest


class CompanyFeedbackForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = ["admin_feedback"]

        widgets = {
            "admin_feedback": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter reason..."
                }
            )
        }
class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = [
            "logo",
            "company_name",
            "email",
            "phone",
            "address",
            "description",
        ]

        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
            }),
        }
class CompanyDocumentForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = ["registration_document"]

        widgets = {
            "registration_document": forms.FileInput(
                attrs={"class": "form-control"}
            ),
        }


class TrekRequestForm(forms.ModelForm):
    class Meta:
        model = TrekRequest
        exclude = [
            "company",
            "status",
            "admin_feedback",
            "created_at",
        ]

        widgets = {
            "trek_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Trek Name",
            }),

            "region": forms.Select(attrs={
                "class": "form-control",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
            }),

            "estimated_altitude": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "difficulty": forms.Select(attrs={
                "class": "form-control",
            }),

            "reference_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }