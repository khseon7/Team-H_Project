from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('signup/', views.signup, name='user_signup'),
    path('login/', views.signin, name='user_login'),
    path('logout/', views.signout, name='user_logout'),
    path('', views.index, name = 'index')
]