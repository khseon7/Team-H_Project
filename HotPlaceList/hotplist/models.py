from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    comment = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    grade = models.FloatField()
    # store = models.ForeignKey(HotPlaces, on_delete = models.CASCADE)
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = '')
    
class HotPlaces(models.Model):
    name = models.CharField(max_length = 100, null = False)
    address = models.CharField(max_length = 200, null = False)
    phone_num = models.CharField(max_length = 15, null = True, blank = True)
    #original_rating = models.DecimalField(max_digits = 2, decimal_places = 1, validators = [validate_rating], default = 0.0)
    #rating = models.DecimalField(max_digits = 2, decimal_places = 1, validators = [validate_rating],default = 0.0)
    image = models.ImageField(upload_to = 'images/')