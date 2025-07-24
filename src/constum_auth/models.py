from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class SaasUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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