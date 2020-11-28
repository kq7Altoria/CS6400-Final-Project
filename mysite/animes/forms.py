from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_id', 'review_content', 'reviewer_id']
