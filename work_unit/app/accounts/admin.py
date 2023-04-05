from django.contrib import admin
from .models import CustomUser, UserProfile
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

admin.site.register(UserProfile, UserProfileAdmin)
