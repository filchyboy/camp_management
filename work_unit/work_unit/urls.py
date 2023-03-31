from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('interviewer/', views.interviewer, name='interviewer'),
    path('interviewee/', views.interviewee, name='interviewee'),
]
