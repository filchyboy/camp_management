from django.shortcuts import render, redirect
from .forms import ProfileImageForm, CustomUserCreationForm, UserProfileForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from .models import CustomUser, UserProfile, Interview, InterviewMention
from allauth.account.utils import send_email_confirmation
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.contrib.auth.decorators import user_passes_test
from .forms import InterviewForm, MentionForm
from django.utils import timezone
import json, os
from django.contrib.auth.decorators import user_passes_test
from django.db import models
from PIL import Image
from django.core.files.storage import default_storage
from .models import get_profile_image_filename
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from .models import AppConfig



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
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')

    else:
        form = UserProfileForm(instance=user_profile)

    interviewee_first_name = ""
    interviewee_last_name = ""
    interviewer_first_name = ""
    interviewer_last_name = ""

    if request.user.profile.assigned_interviewee:
        interviewee_first_name = request.user.profile.assigned_interviewee.profile.first_name
        interviewee_last_name = request.user.profile.assigned_interviewee.profile.last_name

    if request.user.profile.assigned_interviewer:
        interviewer_first_name = request.user.profile.assigned_interviewer.profile.first_name
        interviewer_last_name = request.user.profile.assigned_interviewer.profile.last_name

    context = {
        'form': form,
        'interviewee_first_name': interviewee_first_name,
        'interviewee_last_name': interviewee_last_name,
        'interviewer_first_name': interviewer_first_name,
        'interviewer_last_name': interviewer_last_name,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            image_data = request.POST.get('base64_image')
            image_data = image_data.split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))

            crop_x = int(round(float(request.POST.get('crop_x') or 0)))
            crop_y = int(round(float(request.POST.get('crop_y') or 0)))
            crop_width = int(round(float(request.POST.get('crop_width') or 0)))
            crop_height = int(
                round(float(request.POST.get('crop_height') or 0)))

            # Create a file name for the cropped image
            image_name = get_profile_image_filename(
                profile, 'cropped_image.webp')  # Change the file extension to .webp
            image_path = os.path.join('profile_pics', image_name)

            # Save the cropped image using default_storage
            with BytesIO() as buffer:
                # Change the format to 'WEBP'
                image.save(buffer, format='WEBP')
                buffer.seek(0)
                default_storage.save(image_path, buffer)

            profile.profile_image = image_path
            profile.save()
            messages.success(request, 'Profile photo uploaded successfully.')
            return redirect('accounts:profile')

        else:
            messages.error(request, 'Error uploading profile photo.')
            return redirect('accounts:upload_photo')

    else:
        form = ProfileImageForm(instance=request.user.profile)
        min_crop_dimension = AppConfig.objects.first().min_crop_dimension

    return render(request, 'accounts/upload_photo.html', {'form': form, 'min_crop_dimension': min_crop_dimension})


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

    is_admin = is_administrator(request.user)  # Add this line
    return render(request, 'accounts/admin_dashboard.html', {'users': users, 'is_admin': is_admin})

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

    users = CustomUser.objects.filter(
        profile__category='member', profile__participate=True)
    user_fullnames = [
        f"{user.first_name.strip()} {user.last_name.strip()}".strip() for user in users]

    user_fullnames_json = json.dumps(user_fullnames)

    assigned_interviewee = request.user.profile.assigned_interviewee

    return render(request, 'start_interview.html', {'form': form, 'user_fullnames_json': user_fullnames_json, 'assigned_interviewee': assigned_interviewee})


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


@user_passes_test(is_administrator)
def initiate_interview_process(request):
    eligible_users = CustomUser.objects.annotate(
        is_member=models.Case(
            models.When(profile__category='member', then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField()
        ),
        is_participant=models.Case(
            models.When(profile__participate=True, then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField()
        )
    ).filter(is_member=True, is_participant=True)

    import random
    shuffled_users = random.sample(list(eligible_users), len(eligible_users))

    # Shift the list of shuffled users by one position
    shifted_users = shuffled_users[1:] + shuffled_users[:1]

    # Pair users randomly without self-pairing
    random_pairs = list(zip(shuffled_users, shifted_users))

    # Assign interviewee and interviewer to each user's profile
    for pair in random_pairs:
        interviewer, interviewee = pair
        interviewer.profile.assigned_interviewee = interviewee
        interviewer.profile.save()
        interviewee.profile.assigned_interviewer = interviewer
        interviewee.profile.save()

    return redirect('accounts:interview_process_success')



def interview_process_success(request):
    return render(request, 'accounts/interview_process_success.html')


@login_required
def my_interviews(request):
    profile = request.user.profile
    assigned_interviewee = profile.assigned_interviewee
    assigned_interviewer = profile.assigned_interviewer

    context = {
        'assigned_interviewee': assigned_interviewee,
        'assigned_interviewer': assigned_interviewer,
    }

    return render(request, 'accounts/my_interviews.html', context)


@user_passes_test(is_administrator)
def interview_pairs(request):
    pairs = UserProfile.objects.filter(category='member', participate=True).select_related(
        'assigned_interviewer', 'assigned_interviewee')
    context = {'pairs': pairs}
    return render(request, 'accounts/interview_pairs.html', context)
