from subscriptions.models import Subscription
from django.core.management import BaseCommand
from typing import Any
class Command(BaseCommand):
    def handle(self, *args:Any, **options:Any):
        #print("Hello")
        qs=Subscription.objects.filter(active=True)
        for obj in qs:
            #print(obj.groups.all())
            sub_perm=obj.permissions.all()
            for grp in obj.groups.all():
                grp.permissions.set(sub_perm)
            #     for perm in obj.permission.all():
            #         grp.permissions.add()
            #print(obj.permission.all())