from django import forms
from .models import Profile
from django.contrib.auth.models import User
import re

class UserForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "First Name"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Last Name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "profile-input",
                "placeholder": "Email"
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()

        if not first_name:
            raise forms.ValidationError("First name is required.")

        if len(first_name) < 2:
            raise forms.ValidationError(
                "First name must be at least 2 characters long."
            )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()

        if last_name and len(last_name) < 2:
            raise forms.ValidationError(
                "Last name must be at least 2 characters long."
            )

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not email:
            raise forms.ValidationError("Email is required.")

        if User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "This email is already being used by another account."
            )

        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "phone",
            "date_of_birth",
            "gender",
            "address",
        ]

        widgets = {
            "phone": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Phone Number",
                "inputmode": "tel",
                "pattern": r"\+?[0-9]+",
                "maxlength": "14",
                "oninput": "this.value = this.value.replace(/[^0-9+]/g, '')",
            }),

            "date_of_birth": forms.DateInput(attrs={
                "class": "profile-input",
                "type": "date"
            }),

            "gender": forms.Select(attrs={
                "class": "profile-input"
            }),

            "address": forms.Textarea(attrs={
                "class": "profile-input",
                "rows": 2,
                "placeholder": "Address"
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            return phone

        if not re.fullmatch(r"\+?[0-9]+", phone):
            raise forms.ValidationError(
                "Phone number can only contain numbers and an optional + sign."
            )

        if len(phone) > 14:
            raise forms.ValidationError(
                "Phone number cannot be longer than 14 characters."
            )

        return phone

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if date_of_birth:
            from datetime import date

            if date_of_birth > date.today():
                raise forms.ValidationError(
                    "Date of birth cannot be in the future."
                )

        return date_of_birth

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()
        return address

    class Meta:
        model = Profile

        fields = [
            "phone",
            "date_of_birth",
            "gender",
            "address",
        ]

        widgets = {

            "phone": forms.TextInput(attrs={
                "class": "profile-input",
                "placeholder": "Phone Number"
            }),

            "date_of_birth": forms.DateInput(attrs={
                "class": "profile-input",
                "type": "date"
            }),

            "gender": forms.Select(attrs={
                "class": "profile-input"
            }),

            "address": forms.Textarea(attrs={
                "class": "profile-input",
                "rows": 2,
                "placeholder": "Address"
            }),
        }