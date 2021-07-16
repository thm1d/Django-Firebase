from django.urls import path
from .views import logOutView, createReportView, postCreateReportView, checkReportView, postCheckReportView

urlpatterns = [
    path('logout/', logOutView, name='logout'),
    path('create-report/', createReportView, name='create-report'),
    path('post-create/', postCreateReportView, name='post-create'),
    path('check-report/', checkReportView, name='check-report'),
    path('post-report/<str:key>', postCheckReportView, name='post-report'),
]
