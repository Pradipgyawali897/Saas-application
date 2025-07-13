from django.shortcuts import render
from subscriptions.models import SubscriptionPrice


def show_subscription_view(request):
    monthly_qs=SubscriptionPrice.objects.filter(interval=SubscriptionPrice.IntervallChoices.MONTHLY)
    yearly_qs=SubscriptionPrice.objects.filter(interval=SubscriptionPrice.IntervallChoices.YEAR)

    return render(request,'subscription/subscription.html',context={'monthly_qs':monthly_qs,'yearly_qs':yearly_qs})