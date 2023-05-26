from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_model()
        try:
            user = user.objects.get(email=username)
            if user.check_password(password):
                return user
        except user.DoesNotExist:
            return None

    def get_user(self, user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None
