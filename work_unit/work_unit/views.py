from django.shortcuts import render


def homepage(request):
    return render(request, 'work_unit/homepage.html')


def interviewer(request):
    return render(request, 'work_unit/interviewer.html')


def interviewee(request):
    return render(request, 'work_unit/interviewee.html')
