from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import uuid
from django.contrib.auth import login
from .models import CustomUser, UserProfile
from allauth.account.utils import send_email_confirmation
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.contrib.auth.decorators import user_passes_test



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            # Send email confirmation
            send_email_confirmation(request, user)
            # Log the user in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:additional_information')
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
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            email = request.POST.get('email')  # Get the email from the request
            if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                messages.error(
                    request, 'This email is already in use. Please use a different email address.')
            else:
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                request.user.email = email
                request.user.save()
                user_profile.save()
                # Send the email confirmation
                send_email_confirmation(request, request.user)
                return HttpResponseRedirect(reverse('app.accounts:profile'))
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/additional_information.html', {'form': form})


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.profile.category = 'member'
    user.profile.save()


def is_administrator(user):
    return user.is_authenticated and user.profile.category == 'administrator'


@user_passes_test(is_administrator)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        user_id = request.POST['user_id']
        new_category = request.POST['new_category']
        user = CustomUser.objects.get(pk=user_id)
        user.profile.category = new_category
        user.profile.save()
        messages.success(
            request, f"{user.username}'s category has been updated.")
        return redirect('accounts:admin_dashboard')

    return render(request, 'accounts/admin_dashboard.html', {'users': users})
