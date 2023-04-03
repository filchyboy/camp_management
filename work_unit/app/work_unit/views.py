from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


def homepage(request):
    return render(request, 'work_unit/homepage.html', {
        'register_url': reverse_lazy('app.accounts:register'),
        'login_url': reverse_lazy('app.accounts:login'),
        'logout_url': reverse_lazy('app.accounts:logout'),
    })


def interviewer(request):
    return render(request, 'work_unit/interviewer.html')


def interviewee(request):
    return render(request, 'work_unit/interviewee.html')
