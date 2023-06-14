from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, HotPlaces

class UserForm(UserCreationForm):
    email = forms.EmailField(label = "이메일")
    class Meta:
        model = User
        fields = ['username','password1','password2', 'email']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = HotPlaces
        fields=['name','address','phone_num', 'rating','image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=('comment', 'rating', 'pub_date', 'author', 'store')