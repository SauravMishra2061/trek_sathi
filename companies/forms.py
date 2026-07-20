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