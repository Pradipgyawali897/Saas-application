from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Subscription,UserSubscription,SubscriptionPrice

class UserSubscriptionModel(ModelAdmin):
    list_display=['user','subscription','date']
admin.site.register(UserSubscription,UserSubscriptionModel)



class SubscriptionPriceAdmin(admin.TabularInline):
    model=SubscriptionPrice
    readonly_fields=['stripe_id']
    extra=1

admin.site.register(SubscriptionPrice)

class SubscriptionAdmin(admin.ModelAdmin):
    inlines=[SubscriptionPriceAdmin]
    list_display=['name','active']

admin.site.register(Subscription,SubscriptionAdmin)