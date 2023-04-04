from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful!')
            return redirect(reverse('accounts:profile'))
        else:
            messages.error(
                request, 'There was a problem with your registration. Please check the form and try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def additional_information(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            request.user.email = form.cleaned_data['email']  # Add this line
            request.user.save()  # Add this line
            user_profile.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserProfileForm()
    return render(request, 'accounts/additional_information.html', {'form': form})
