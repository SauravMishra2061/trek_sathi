from django import forms


class TrekRequestReviewForm(forms.Form):

    admin_feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter feedback..."
            }
        )
    )