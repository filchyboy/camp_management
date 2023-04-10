from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
import os

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'), unique=True, blank=True, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username


def get_profile_image_filename(instance, filename):
    first_name = slugify(instance.user.first_name)
    last_name = slugify(instance.user.last_name)
    _, ext = os.path.splitext(filename)
    return f"profile_pics/profile_{first_name}_{last_name}{ext}"


class UserProfile(models.Model):
    USER_CATEGORY_CHOICES = [
        ('member', 'Member'),
        ('removed_member', 'Removed Member'),
        ('camper', 'Camper'),
        ('observer', 'Observer'),
        ('administrator', 'Administrator'),
    ]
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    category = models.CharField(
        choices=USER_CATEGORY_CHOICES, default='member', max_length=30)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    participate = models.BooleanField(default=False)

    assigned_interviewee = models.ForeignKey(
        CustomUser, related_name='assigned_interviewee', null=True, on_delete=models.SET_NULL)
    assigned_interviewer = models.ForeignKey(
        CustomUser, related_name='assigned_interviewer', null=True, on_delete=models.SET_NULL)

    # Add your new fields here:
    legal_name = models.CharField(max_length=255, blank=True)
    playa_name = models.CharField(max_length=255, blank=True)
    staging_date = models.DateField(null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    departure_staging_date = models.DateField(null=True, blank=True)
    hash_id = models.CharField(max_length=255, blank=True)
    arrival_staging_location = models.CharField(max_length=255, blank=True)
    departure_staging_location = models.CharField(max_length=255, blank=True)
    ride_share_status = models.CharField(max_length=255, blank=True)
    camp_score = models.CharField(max_length=255, blank=True)
    work_unit = models.CharField(max_length=255, blank=True)
    work_unit_average = models.CharField(max_length=255, blank=True)
    camp_class = models.CharField(max_length=255, blank=True)

    profile_image = ProcessedImageField(upload_to=get_profile_image_filename,
                                processors=[ResizeToFill(600, 600)],
                                format='WEBP',
                                options={'quality': 90},
                                default='default.jpg')

    def __str__(self):
        return f"{self.user.username}'s profile"




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Interview(models.Model):
    interviewer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='interviews')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Interview by {self.interviewer}"


class InterviewMention(models.Model):
    interview = models.ForeignKey(
        Interview, on_delete=models.CASCADE, related_name='mentions')
    mentioned_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='mentions')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.mentioned_user} mentioned {self.count} times"


class AppConfig(models.Model):
    min_crop_dimension = models.PositiveIntegerField(default=300)

    class Meta:
        verbose_name_plural = 'App Configurations'

    def __str__(self):
        return f'Minimum Crop Dimension: {self.min_crop_dimension}'
