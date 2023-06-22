from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "hotplist"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('detail/<int:HP_id>/',views.detail,name="detail"),
    path('review/new/<int:HP_id>/',views.new_review,name="new_review"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name='logout'),
]