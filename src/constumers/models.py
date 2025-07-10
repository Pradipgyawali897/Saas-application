from django.db import models
from django.contrib.auth.models import User
import helpers
import helpers.billing
from allauth.account.signals import user_signed_up as allauth_user_signed_up,email_confirmed as allauth_email_confirmed

class Constumer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    init_email=models.EmailField(blank=True,null=True)
    init_email_confirmed=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.stripe_id:
            if self.init_email_confirmed and self.init_email:
                email = self.init_email
                if email:
                    response = helpers.billing.create_customer(
                        name=self.user.username,
                        email=email,
                        raw=False,
                        metadata={'user_id':self.user.id,'uesrname':self.user.username},
                    )
                    self.stripe_id = response.id
        return super().save(*args, **kwargs)
def allauth_user_signed_up_handler(request,user,*args, **kwargs):
    email=user.email
    Constumer.objects.create(
        user=user,
        init_email=email,
        init_email_confirmed=True,

    )

allauth_user_signed_up.connect(allauth_user_signed_up_handler)

def allauth_email_confirmed_handler(request,user,*args, **kwargs):
    qs=Constumer.objects.filter(
        user=user,
        init_email_confirmed=True,
    )
    for obj in qs:
        obj.init_email_confirmed=True
        obj.save()

allauth_email_confirmed.connect(allauth_email_confirmed_handler)