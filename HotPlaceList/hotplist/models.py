from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class HotPlace(models.Model):
    placename=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    callnum=models.CharField(max_length=20)
    eval=models.DecimalField(max_digits=5,decimal_places=1)
    image=models.ImageField(upload_to='images/')
    
class WantList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="")
    hotplace=models.ForeignKey(HotPlace,on_delete=models.CASCADE,default="")

class Review(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,default="")
    content=models.CharField()
    hotplace=models.ForeignKey(HotPlace,on_delete=models.CASCADE,)
    eval=models.DecimalField(max_digits=5,decimal_places=1)
    date=models.DateTimeField()
    