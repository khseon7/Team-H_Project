from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    comment = models.CharField(max_length=200)
    grade = models.DecimalField(max_digits=1, decimal_places=1,)
    store = models.ForeignKey
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = '')