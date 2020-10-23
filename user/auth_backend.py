from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import transaction

from .models import UserProfile

User = get_user_model()

class UserProfileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            with transaction.atomic():
                user = User._default_manager.get_by_natural_key(username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    if not UserProfile.objects.filter(user=user).exists():
                        userprofile = UserProfile.objects.create(user=user)
                    return user
                else:
                    return None
        except User.DoesNotExist:
            return super().authenticate(request=request, username=username, password=password)