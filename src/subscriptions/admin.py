from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Subscription,UserSubscription

admin.site.register(Subscription)
class UserSubscriptionModel(ModelAdmin):
    list_display=['user','subscription','date']
admin.site.register(UserSubscription,UserSubscriptionModel)