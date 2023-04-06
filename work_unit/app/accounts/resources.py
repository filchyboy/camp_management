from import_export import resources
from .models import UserProfile


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile
