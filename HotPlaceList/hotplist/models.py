from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HotPlaces(models.Model):
    name = models.CharField(max_length = 100, null = False)
    address = models.CharField(max_length = 200, null = False)
    phone_num = models.CharField(max_length = 15, null = True, blank = True)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2)
    image = models.ImageField(upload_to = 'images/')


class SavedPlaces(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    saved = models.ForeignKey(HotPlaces, on_delete = models.CASCADE)


class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length = 400, null = False)
    place = models.ForeignKey(HotPlaces, on_delete = models.CASCADE)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, null = True)
    pub_date = models.DateTimeField()


