from django.contrib import admin
from django.urls import path
from .views import indexView, authView, profileView

urlpatterns = [
    path('', indexView, name='home'),
    path('login/', authView, name='auth'),
    path('profile/', profileView, name='profile'),
]
