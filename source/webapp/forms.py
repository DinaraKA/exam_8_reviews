from django import forms

from webapp.models import Review


class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', 'rating']