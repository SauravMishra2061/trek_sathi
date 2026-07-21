from django import forms
from .models import Company


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