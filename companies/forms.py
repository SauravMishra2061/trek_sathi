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
            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                    "inputmode": "tel",
                    "pattern": r"\+?[0-9]+",
                    "maxlength": "14",
                    "oninput": (
                        "this.value = "
                        "this.value.replace(/[^0-9+]/g, '')"
                    ),
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Address",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell us about your company",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_company_name(self):
        company_name = self.cleaned_data.get(
            "company_name", ""
        ).strip()

        if not company_name:
            raise forms.ValidationError(
                "Company name is required."
            )

        if len(company_name) < 2:
            raise forms.ValidationError(
                "Company name must be at least 2 characters long."
            )

        return company_name

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            return email

        return email.strip().lower()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        import re

        if not re.fullmatch(r"\+?[0-9]+", phone):
            raise forms.ValidationError(
                "Phone number can only contain numbers "
                "and an optional + sign."
            )

        if len(phone) > 14:
            raise forms.ValidationError(
                "Phone number cannot be longer than 14 characters."
            )

        return phone

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()
        return address

    def clean_description(self):
        description = self.cleaned_data.get(
            "description", ""
        ).strip()

        return description
class CompanyDocumentForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = ["registration_document"]

        widgets = {
            "registration_document": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png",
                }
            ),
        }

    def clean_registration_document(self):
        document = self.cleaned_data.get("registration_document")

        # No file selected
        if not document:
            raise forms.ValidationError(
                "Please select a registration document."
            )

        # Maximum size: 5 MB
        max_size = 5 * 1024 * 1024

        if document.size > max_size:
            raise forms.ValidationError(
                "File size cannot exceed 5 MB."
            )

        # Allowed file extensions
        allowed_extensions = [
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
        ]

        filename = document.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions
        ):
            raise forms.ValidationError(
                "Only PDF, JPG, JPEG, and PNG files are allowed."
            )

        return document
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
                "placeholder": "Describe the trek...",
            }),

            "estimated_altitude": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 5416",
                "min": "1",
            }),

            "difficulty": forms.Select(attrs={
                "class": "form-control",
            }),

            "reference_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".jpg,.jpeg,.png",
            }),
        }

    def clean_trek_name(self):
        trek_name = self.cleaned_data.get("trek_name", "").strip()

        if not trek_name:
            raise forms.ValidationError(
                "Trek name is required."
            )

        if len(trek_name) < 3:
            raise forms.ValidationError(
                "Trek name must be at least 3 characters long."
            )

        return trek_name

    def clean_description(self):
        description = self.cleaned_data.get(
            "description", ""
        ).strip()

        if not description:
            raise forms.ValidationError(
                "Trek description is required."
            )

        if len(description) < 20:
            raise forms.ValidationError(
                "Description must be at least 20 characters long."
            )

        return description

    def clean_estimated_altitude(self):
        altitude = self.cleaned_data.get("estimated_altitude")

        if altitude is not None and altitude <= 0:
            raise forms.ValidationError(
                "Altitude must be greater than 0 meters."
            )

        return altitude

    def clean_reference_image(self):
        image = self.cleaned_data.get("reference_image")

        if not image:
            return image

        # Maximum image size: 5 MB
        max_size = 5 * 1024 * 1024

        if image.size > max_size:
            raise forms.ValidationError(
                "Reference image cannot exceed 5 MB."
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