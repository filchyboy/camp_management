from django.contrib import admin
from .models import CustomUser, UserProfile, Interview, InterviewMention
from .forms import UserProfileForm, AdminUserProfileForm
from import_export.admin import ImportExportModelAdmin
from .resources import UserProfileResource


admin.site.register(CustomUser)


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    fields = ('user', 'category', 'first_name',
              'last_name', 'phone_number', 'participate')
    list_display = ('user', 'category', 'first_name',
                    'last_name', 'phone_number', 'participate')
    search_fields = ('user__username', 'first_name', 'last_name')


class UserProfileAdmin(admin.ModelAdmin):
    form = AdminUserProfileForm
    fields = (
        'user', 'category', 'first_name', 'last_name', 'phone_number', 'participate',
        'legal_name', 'playa_name', 'staging_date', 'arrival_date', 'departure_date',
        'departure_staging_date', 'hash_id', 'arrival_staging_location',
        'departure_staging_location', 'ride_share_status', 'camp_score', 'work_unit',
        'work_unit_average', 'camp_class',
    )
    list_display = ('user', 'category', 'first_name',
                    'last_name', 'phone_number', 'participate')
    search_fields = ('user__username', 'first_name', 'last_name')


class UserProfileAdmin(ImportExportModelAdmin):
    form = AdminUserProfileForm
    resource_class = UserProfileResource
    fields = (
        'user', 'category', 'first_name', 'last_name', 'phone_number', 'participate',
        'legal_name', 'playa_name', 'staging_date', 'arrival_date', 'departure_date',
        'departure_staging_date', 'hash_id', 'arrival_staging_location',
        'departure_staging_location', 'ride_share_status', 'camp_score', 'work_unit',
        'work_unit_average', 'camp_class',
    )
    list_display = ('user', 'category', 'first_name',
                    'last_name', 'phone_number', 'participate')
    search_fields = ('user__username', 'first_name', 'last_name')
    # Add any other fields you want to filter by
    list_filter = ('category', 'participate', 'arrival_date', 'departure_date')
    # Add any other fields you want to edit
    list_editable = ('category', 'participate')
    list_per_page = 25
    ordering = ('user',)  # Default ordering


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('interviewer', 'start_time', 'end_time')
    search_fields = ('interviewer__username', 'start_time', 'end_time')
    list_filter = ('interviewer', 'start_time', 'end_time')


class InterviewMentionAdmin(admin.ModelAdmin):
    list_display = ('interview', 'mentioned_user', 'count')
    search_fields = ('interview__interviewer__username',
                     'mentioned_user__username')
    list_filter = ('interview__interviewer', 'mentioned_user')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(InterviewMention, InterviewMentionAdmin)
