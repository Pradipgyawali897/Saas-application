from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import helpers
import helpers.billing
from django.core.exceptions import ValidationError

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
    stripe_id = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None and not self.stripe_id
        super().save(*args, **kwargs)

        if is_new:
            try:
                stripe_id = helpers.billing.create_product(
                    name=self.name,
                    metadata={"subscription_plan_id": self.id}
                )
                self.stripe_id = stripe_id
                super().save(update_fields=['stripe_id'])
            except Exception as e:
                from django.core.exceptions import ValidationError
                raise ValidationError(f"Stripe product creation failed: {e}")


class SubscriptionPrice(models.Model):
    class IntervallChoices(models.TextChoices):
        MONTHLY = "month", "MONTHLY"
        YEAR = "year", "Year"

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_id = models.CharField(max_length=150, blank=True, null=True)
    interval = models.CharField(max_length=120, default=IntervallChoices.MONTHLY, choices=IntervallChoices.choices)
    price = models.DecimalField(max_digits=13, decimal_places=2, default=99.99)

    @property
    def stripe_price(self):
        return int(self.price * 100)

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        if self.stripe_id is None and self.product_stripe_id is not None:
            stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                recurring=self.interval,  # Pass string, not dict
                product=self.product_stripe_id,
                metadata={"subscription_plan_id": self.id},
            )
            if not stripe_id:
                raise ValidationError("Stripe price creation failed: No price ID returned.")
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)


    def __str__(self):
        return self.subscription.name if self.subscription else "No Subscription"    





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