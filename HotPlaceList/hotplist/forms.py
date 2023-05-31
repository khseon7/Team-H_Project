from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

REVIEW_POINT_CHOICES = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=('comment', 'grade', 'store', 'pub_date', 'author')
        widgets = {
            'grade': forms.Select(choices=REVIEW_POINT_CHOICES)
        }