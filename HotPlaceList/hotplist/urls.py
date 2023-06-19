from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create/', views.create, name = 'create'),
    path('details/<int:HP_id>',views.details, name = 'details'),
    path('comment/create/<int:HP_id>',views.comment_create, name = 'comment_create'),
    path('comment/edit/<int:Review_id>/',views.comment_edit, name = 'comment_edit'),
    path('comment/delete/<int:Review_id>/', views.comment_delete, name = 'comment_delete'),
    path('signup/',views.signup, name = 'signup'),
    path('logout/',views.logout, name = 'logout'),
    path('login/',views.login, name = "login"),
    path('profile/<int:HP_author>/', views.profile, name='profile'),
    path('save/<int:HP_id>/',views.save, name = "save"),
    path('save/delete/<int:HP_id>/',views.save_delete, name = 'save_delete'),
    
]