from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.db.models.signals import post_save


SUBSCRIPTION_PERMISSIONS =  [
        ('advanced', "Advanced Permission"),
        ('pro', "Pro Permission"),
        ('basic', "Basic Permission")
    ]

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            'content_type__app_label': 'subscriptions',
            'codename__in': [x[0] for x in SUBSCRIPTION_PERMISSIONS]
        }
    )

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

    def __str__(self):
        return self.name



class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)  
    date = models.DateTimeField(verbose_name="Date Of subscription", auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
def user_sub_post_signal(sender, instance, *args, **kwargs):
    subscription_obj = instance.subscription
    user = instance.user

    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        user.groups.set(groups)
    else:
        user.groups.clear()

post_save.connect(user_sub_post_signal,sender=UserSubscription)