from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register_view, name='register'),
    path("login/", views.login_site , name='login_site'),
    path('friend_list/' , views.friends_list, name='friend_list')
]
