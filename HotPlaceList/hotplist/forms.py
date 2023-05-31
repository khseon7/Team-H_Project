from django import forms
from hotplist.models import HotPlaces,Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
## form 내부에 fields에 있는 값들은 POST 모델에서 입력받고 싶은 필드를 리스트 형태로 작성
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

class HPForm(forms.ModelForm):
    class Meta:
        model=HotPlaces
        fields=["placename","address","phone","rating","image"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=["content","rating"]