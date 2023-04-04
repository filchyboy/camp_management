from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'), unique=True, blank=True, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username


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

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
