from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission
from django.utils import timezone
from datetime import timedelta
import random


class SaasUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(verbose_name="password",max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the raw password matches the stored hash."""
        return check_password(raw_password, self.password_hash)

    def save(self, *args, **kwargs):
        """Optional: Ensure password is hashed before saving if modified."""
        # Only hash if password_hash is set and not already hashed
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.set_password(self.password_hash)
        super().save(*args, **kwargs)


class OTP(models.Model):
    user = models.ForeignKey('SaasUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)  
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField()
    
    
    def is_expired(self):
        return timezone.now() > self.expiry_time

    def save(self, *args, **kwargs):
        def generate_otp():
            return str(random.randint(100000, 999999))
        self.code=generate_otp()
        if not self.expiry_time:
            self.expiry_time = timezone.now() + timedelta(minutes=5)
        
        
        super().save(*args, **kwargs)
    