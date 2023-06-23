from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

def validate_rating(value):
    if value >5.0 or value<0.0:
        raise ValidationError(
            ('0.0에서 5.0 사이 값을 입력해주세요')
        )

# Create your models here.
class HotPlaces(models.Model):
    placename=models.CharField(max_length=100,null=False)
    address=models.CharField(max_length=120,null=False)
    phone=models.CharField(max_length=15,null=True,blank=True)
    origin_rating=models.DecimalField(max_digits=2,decimal_places=1,validators=[validate_rating],default=0.0)
    rating=models.DecimalField(max_digits=2,decimal_places=1,validators=[validate_rating],default=0.0)
    image=models.ImageField(upload_to='images/')
    
class WantList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    hotplace=models.ForeignKey(HotPlaces,on_delete=models.CASCADE)

class Review(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.CharField(max_length=200,null=True)
    place=models.ForeignKey(HotPlaces,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=2,decimal_places=1,validators=[validate_rating])
    date=models.DateTimeField()