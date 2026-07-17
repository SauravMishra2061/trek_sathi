from django import forms
from .models import Profile
from django.contrib.auth.models import User

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
                "rows": 3,
                "placeholder": "Address"
            }),
        }