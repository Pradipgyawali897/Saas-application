# app/auth_backends.py
from .models import SaasUser
from django.contrib.auth.backends import BaseBackend

class SaasUserBackend(BaseBackend):
    def authenticate(self, request, Email=None, password=None):
        try:
            user = SaasUser.objects.get(Email=Email)
            if user.check_password(password):
                return user
        except SaasUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return SaasUser.objects.get(pk=user_id)
        except SaasUser.DoesNotExist:
            return None
