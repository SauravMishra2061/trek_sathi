from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["rating"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["rating"].widget = forms.RadioSelect(
            choices=Review.RATING_CHOICES
        )