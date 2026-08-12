from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["message"]

        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Type your message..."
                }
            )
        }

class EnquiryForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Subject"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 6,
            "placeholder": "Type your enquiry..."
        })
    )