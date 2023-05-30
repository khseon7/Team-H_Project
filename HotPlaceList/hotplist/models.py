from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
def validate_rating(value):
    if value > 5.0 or value < 0.0:
        raise ValidationError(
            ('5.0에서 0.0 사이의 값을 입력해주세요'),
        )
    

class HotPlaces(models.Model):
    name = models.CharField(max_length = 100, null = False)
    address = models.CharField(max_length = 200, null = False)
    phone_num = models.CharField(max_length = 15, null = True, blank = True)
    original_rating = models.DecimalField(max_digits = 2, decimal_places = 1, validators = [validate_rating], default = 0.0)
    rating = models.DecimalField(max_digits = 2, decimal_places = 1, validators = [validate_rating],default = 0.0)
    image = models.ImageField(upload_to = 'images/')


class SavedPlaces(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    saved = models.ForeignKey(HotPlaces, on_delete = models.CASCADE)


class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length = 400, null = False)
    place = models.ForeignKey(HotPlaces, on_delete = models.CASCADE)
    rating = models.DecimalField(max_digits = 2, decimal_places = 1, validators = [validate_rating])
    pub_date = models.DateTimeField()


