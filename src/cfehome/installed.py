# installed.py

Django_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "slippers",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

APPS = Django_APPS + [
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "widget_tweaks",
]

CUSTOMER_INSTALLED_APPS = APPS + [
    "commando",
    "profiles",
    "visits",
]

INSTALLED_APPS = APPS + [
    "constum_auth",
    "tenants",
    "commando",
    "customers",
    "profiles",
    "subscriptions",
    "visits",
]

_INSTALLED_APPS = list(set(INSTALLED_APPS))
CONSTUMER_INSTALLED_APPS = list(set(CUSTOMER_INSTALLED_APPS))

SHARED_APPS = (
    "constum_auth",
    "tenants",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
)

TENANT_APPS = (
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "slippers",
    "allauth_ui",
    "widget_tweaks",
    "commando",
    "customers",
    "profiles",
    "subscriptions",
    "visits",
)