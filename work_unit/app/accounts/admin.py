from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from .models import CustomUser, UserProfile, Interview, InterviewMention
from .forms import UserProfileForm, AdminUserProfileForm
from import_export.admin import ImportExportModelAdmin
from .resources import UserProfileResource
from . import views


admin.site.register(CustomUser)


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
    list_filter = ('category', 'participate', 'arrival_date', 'departure_date')
    list_editable = ('category', 'participate')
    list_per_page = 25
    ordering = ('user',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('initiate_interview_process/', self.admin_site.admin_view(
                views.initiate_interview_process), name='initiate_interview_process'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['initiate_interview_process_url'] = reverse(
            'admin:initiate_interview_process')
        return super(UserProfileAdmin, self).changelist_view(request, extra_context=extra_context)


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
