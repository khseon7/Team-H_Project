from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_articles')

class Review(models.Model):
    comment = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    store = models.ForeignKey(HotPlaces, on_delete = models.CASCADE, null = False)
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = '')
