from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission
from django.utils import timezone
import random
import string
from constum_auth.validate.otp import send_otp,validate_otp

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
        send_otp(self)
        validate_otp()

class OTP(models.Model):
    PURPOSE_CHOICES = [
        ('login', 'Login'),
        ('email_verification', 'Email Verification'),
    ]
    
    user = models.ForeignKey(SaasUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default='000000')
    expiry_time = models.DateTimeField()
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.digits, k=6))
        if not self.expiry_time:
            self.expiry_time = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)
    