from django import forms
import re

from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = [
            "number_of_people",
            "emergency_contact",
            "special_request",
        ]

        widgets = {

            "number_of_people": forms.NumberInput(
                attrs={
                    "min": 1,
                    "class": "form-control",
                    "placeholder": "Number of People",
                }
            ),

            "emergency_contact": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Emergency Contact Number",
                    "maxlength": "14",
                    "inputmode": "tel",
                }
            ),

            "special_request": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Special requests (optional)",
                }
            ),
        }

    # =====================================
    # NUMBER OF PEOPLE VALIDATION
    # =====================================

    def clean_number_of_people(self):

        number = self.cleaned_data.get(
            "number_of_people"
        )

        if number is None:

            raise forms.ValidationError(
                "Please enter the number of people."
            )

        if number < 1:

            raise forms.ValidationError(
                "Number of people must be at least 1."
            )

        return number


    # =====================================
    # EMERGENCY CONTACT VALIDATION
    # =====================================

    def clean_emergency_contact(self):

        phone = (
            self.cleaned_data.get(
                "emergency_contact",
                ""
            )
            .strip()
        )

        if not phone:

            raise forms.ValidationError(
                "Emergency contact number is required."
            )

        # =====================================
        # ALLOW ONLY + AT THE START
        # AND NUMBERS
        # =====================================

        if not re.fullmatch(
            r"\+?[0-9]+",
            phone
        ):

            raise forms.ValidationError(
                "Emergency contact can contain only numbers and an optional + at the beginning."
            )

        # =====================================
        # LENGTH VALIDATION
        # =====================================

        if len(phone) > 14:

            raise forms.ValidationError(
                "Emergency contact cannot exceed 14 characters."
            )

        # =====================================
        # PREVENT ONLY +
        # =====================================

        if phone == "+":

            raise forms.ValidationError(
                "Please enter a valid emergency contact number."
            )

        return phone


    # =====================================
    # SPECIAL REQUEST VALIDATION
    # =====================================

    def clean_special_request(self):

        special_request = (
            self.cleaned_data.get(
                "special_request",
                ""
            )
            .strip()
        )

        return special_request