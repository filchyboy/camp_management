from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'app.accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('additional_information/', views.additional_information,
         name='additional_information'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('initiate_interview_process/', views.initiate_interview_process,
         name='initiate_interview_process'),
    path('interview_process_success/', views.interview_process_success,
         name='interview_process_success'),
    path('my_interviews/', views.my_interviews, name='my_interviews'),
    path('interview_pairs/', views.interview_pairs, name='interview_pairs'),

]

