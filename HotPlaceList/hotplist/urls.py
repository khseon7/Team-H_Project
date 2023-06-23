from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('detail/<int:HP_id>/',views.detail,name="detail"),
    path('review/new/<int:HP_id>/',views.new_review,name="new_review"),
    path('review/edit/<int:Review_id>/',views.edit_review,name="edit_review"),
    path('review/delete/<int:Review_id>/',views.delete_review,name="delete_review"),
    path('my_profile/',views.my_profile,name="my_profile"),
    path('hotplace/new/',views.new_place,name="new_place"),
    path('hotplace/delete/<int:HP_id>/',views.delete_place,name="delete_place"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name='logout'),
]