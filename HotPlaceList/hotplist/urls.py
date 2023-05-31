from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create/', views.create, name = 'create'),
    path('details/<int:HP_id>',views.details, name = 'details'),
    path('comment/create/<int:HP_id>',views.comment_create, name = 'comment_create'),
    path('signup/',views.signup, name = 'signup'),
    
]