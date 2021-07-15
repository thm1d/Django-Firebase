from django.contrib import admin
from django.urls import path
from .views import indexView, registerView, postRegisterView, authView, profileView, logOutView, createReportView, postCreateReportView, checkReportView, postCheckReportView

urlpatterns = [
    path('', indexView, name='home'),
    path('register/', registerView, name='register'),
    path('post-register/', postRegisterView, name='post-register'),
    path('login/', authView, name='auth'),
    path('profile/', profileView, name='profile'),
    path('logout/', logOutView, name='logout'),
    path('create-report/', createReportView, name='create-report'),
    path('post-create/', postCreateReportView, name='post-create'),
    path('check-report/', checkReportView, name='check-report'),
    path('post-report/<str:key>', postCheckReportView, name='post-report'),
]
