from django.contrib import admin
from .models import HotPlaces, SavedPlaces, Reviews

# Register your models here.
admin.site.register(HotPlaces)
admin.site.register(SavedPlaces)
admin.site.register(Reviews)