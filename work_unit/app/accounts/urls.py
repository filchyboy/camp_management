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
]

