from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, Interview


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['category']
        fields = (
            'first_name', 'last_name', 'phone_number', 'participate', 'category',
            'legal_name', 'playa_name', 'staging_date', 'arrival_date', 'departure_date',
            'departure_staging_date', 'hash_id', 'arrival_staging_location',
            'departure_staging_location', 'ride_share_status', 'camp_score', 'work_unit',
            'work_unit_average', 'camp_class', 'profile_image'
        )


class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'user', 'category', 'first_name', 'last_name', 'phone_number', 'participate',
            'legal_name', 'playa_name', 'staging_date', 'arrival_date', 'departure_date',
            'departure_staging_date', 'hash_id', 'arrival_staging_location',
            'departure_staging_location', 'ride_share_status', 'camp_score', 'work_unit',
            'work_unit_average', 'camp_class',
        )

# forms.py


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ('interviewer',)


class MentionForm(forms.Form):
    mentioned_user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    count = forms.IntegerField(min_value=1)
