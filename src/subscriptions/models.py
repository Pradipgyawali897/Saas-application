from django.db import models
from django.contrib.auth.models import Group,Permission
SUBSCRIPTION_PERMISSIONS=[
            ('advanced',"Advanced Permission"),
            ('pro',"Pro Permission"),
            ('basic',"basic permission")
        ]

class Subscription(models.Model):
    name=models.CharField(max_length=120)
    groups=models.ManyToManyField(Group)
    permission=models.ManyToManyField(Permission,limit_choices_to={'content_type__app_label':'subscriptions','codename__in':[x[0] for x in SUBSCRIPTION_PERMISSIONS]})
    class Meta:
        permissions=SUBSCRIPTION_PERMISSIONS
    def __str__(self):
        return self.name
    