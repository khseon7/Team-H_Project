from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create/', views.create, name = 'create'),
    path('detail/<int:HP_id>',views.detail, name = 'detail'),
    path('review/create/<int:HP_id>',views.review_create, name = 'review_create'),
    path('review/edit/<int:item_id>/',views.review_modify, name = 'review_modify'),
    path('review/delete/<int:item_id>/', views.review_delete, name = 'review_delete'),
    path('signup/',views.signup, name = 'signup'),
    path('logout/',views.logout, name = 'logout'),
    path('login/',views.login, name = "login"),
    path('like/<int:HP_id>/',views.like, name = "like"),
    path('profile/',views.profile, name = "profile"),
]