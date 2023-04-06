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
from .models import Interview, InterviewMention
from .forms import InterviewForm, MentionForm
from django.utils import timezone
import json
from django.core.serializers import serialize



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
            # Get the first name from the request
            first_name = request.POST.get('first_name')
            # Get the last name from the request
            last_name = request.POST.get('last_name')

            if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                messages.error(
                    request, 'This email is already in use. Please use a different email address.')
            else:
                user_profile = form.save(commit=False)
                user_profile.user = request.user

                # Update the user's first name, last name, and email
                request.user.first_name = first_name
                request.user.last_name = last_name
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


def start_interview(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interviewed_users = request.POST.getlist('interviewed_users[]')
            interview = form.save(commit=False)
            interview.start_time = timezone.now()
            interview.save()
            for user_id in interviewed_users:
                user = CustomUser.objects.get(pk=user_id)
                mention, _ = InterviewMention.objects.get_or_create(
                    interview=interview, mentioned_user=user)
                mention.count += 1
                mention.save()
            return redirect('add_tags')
    else:
        form = InterviewForm(initial={'interviewer': request.user})

    users = CustomUser.objects.all()
    user_fullnames = [
        f"{user.first_name.strip()} {user.last_name.strip()}".strip() for user in users]

    print("User full names:", user_fullnames)  # Log user_fullnames

    user_fullnames_json = json.dumps(user_fullnames)

    return render(request, 'start_interview.html', {'form': form, 'user_fullnames_json': user_fullnames_json})


def end_interview(request):
    interview_id = request.session.get('interview_id')
    if interview_id:
        interview = Interview.objects.get(pk=interview_id)
        interview.end_time = timezone.now()
        interview.save()
        del request.session['interview_id']
    return redirect(reverse('app.accounts:profile'))


def add_tags(request):
    interview_id = request.session.get('interview_id')
    if not interview_id:
        return redirect('start_interview')

    if request.method == 'POST':
        form = MentionForm(request.POST)
        if form.is_valid():
            interview = Interview.objects.get(pk=interview_id)
            mentioned_user = form.cleaned_data['mentioned_user']
            count = form.cleaned_data['count']
            mention, created = InterviewMention.objects.get_or_create(
                interview=interview, mentioned_user=mentioned_user)
            mention.count += count
            mention.save()
            return redirect('add_tags')
    else:
        form = MentionForm()
    return render(request, 'add_tags.html', {'form': form})
