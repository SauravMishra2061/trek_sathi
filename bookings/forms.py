from django import forms
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
                }
            ),

            "emergency_contact": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Emergency Contact Number",
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