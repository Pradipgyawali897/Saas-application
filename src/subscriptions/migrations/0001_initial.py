# Generated by Django 5.0.14 on 2025-07-28 10:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('subtitle', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('order', models.IntegerField(default=-1, help_text='Ordering on Django pricing page')),
                ('featured', models.BooleanField(default=True, help_text='Featured on Django pricing page')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('features', models.TextField(blank=True, help_text='Features for pricing, seperated by new line', null=True)),
                ('groups', models.ManyToManyField(to='auth.group')),
                ('permissions', models.ManyToManyField(limit_choices_to={'codename__in': ['advanced', 'pro', 'basic', 'basic_ai'], 'content_type__app_label': 'subscriptions'}, to='auth.permission')),
            ],
            options={
                'ordering': ['order', 'featured', '-updated'],
                'permissions': [('advanced', 'Advanced Perm'), ('pro', 'Pro Perm'), ('basic', 'Basic Perm'), ('basic_ai', 'Basic AI Perm')],
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('interval', models.CharField(choices=[('month', 'Monthly'), ('year', 'Yearly')], default='month', max_length=120)),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=10)),
                ('order', models.IntegerField(default=-1, help_text='Ordering on Django pricing page')),
                ('featured', models.BooleanField(default=True, help_text='Featured on Django pricing page')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('subscription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.subscription')),
            ],
            options={
                'ordering': ['subscription__order', 'order', 'featured', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('active', models.BooleanField(default=True)),
                ('user_cancelled', models.BooleanField(default=False)),
                ('original_period_start', models.DateTimeField(blank=True, null=True)),
                ('current_period_start', models.DateTimeField(blank=True, null=True)),
                ('current_period_end', models.DateTimeField(blank=True, null=True)),
                ('cancel_at_period_end', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, choices=[('active', 'Active'), ('trialing', 'Trialing'), ('incomplete', 'Incomplete'), ('incomplete_expired', 'Incomplete Expired'), ('past_due', 'Past Due'), ('canceled', 'Canceled'), ('unpaid', 'Unpaid'), ('paused', 'Paused')], max_length=20, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.subscription')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
