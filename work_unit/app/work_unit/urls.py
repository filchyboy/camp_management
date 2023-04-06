from django.urls import include, path
from . import views

app_name = 'work_unit'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('interviewer/', views.interviewer, name='interviewer'),
    path('interviewee/', views.interviewee, name='interviewee'),
    path('accounts/', include('app.accounts.urls', namespace='accounts')),
]
