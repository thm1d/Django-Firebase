from django.contrib import admin
from django.urls import path
from .views import indexView, registerView, postRegisterView, authView, profileView, logOutView

urlpatterns = [
    path('', indexView, name='home'),
    path('register/', registerView, name='register'),
    path('post-register/', postRegisterView, name='post-register'),
    path('login/', authView, name='auth'),
    path('profile/', profileView, name='profile'),
    path('logout/', logOutView, name='logout'),
]
