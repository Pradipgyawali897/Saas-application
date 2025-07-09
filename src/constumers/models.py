from django.db import models
from django.contrib.auth.models import User
import helpers
import helpers.billing
class Constumer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    stripe_id=models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.user.username
    def save(self,*args, **kwargs):
        stripe_id=helpers.billing.create_consumer(raw=True)
        return super().save(*args, **kwargs)