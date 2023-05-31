from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('detail/', views.index, name = 'review_create'),
]