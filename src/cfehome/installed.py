

Django_APPS=[
    # django-apps
    "django.contrib.admin",
    "django.contrib.auth",
    'slippers',
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles", 
  
]
APPS=Django_APPS+[
      # third-party-apps
    "allauth_ui",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    "widget_tweaks",
]


_CONSTUMER_INSTALLED_APPS=APPS+[
    # my-apps
    "commando",
    "profiles",
    "visits",
]



_INSTALLED_APPS=APPS+[
    # my-apps
    "commando",
    "customers",
    "customers",
    "profiles",
    "subscriptions",
    "visits",
    "tenants",
]


_INSTALLED_APPS=list(set(_INSTALLED_APPS)) #filter to remove the dupllicate
CONSTUMER_INSTALLED_APPS=list(set(_CONSTUMER_INSTALLED_APPS))