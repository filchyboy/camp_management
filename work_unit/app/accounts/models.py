from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
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

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
