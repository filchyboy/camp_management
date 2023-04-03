from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful!')
            return redirect(reverse('work_unit:homepage'))
        else:
            messages.error(
                request, 'There was a problem with your registration. Please check the form and try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
