from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_id', 'review_content', 'reviewer_id']

# class SearchForm(forms.Form):
#     keyword = forms.CharField(label='Key Word', max_length = 200)
