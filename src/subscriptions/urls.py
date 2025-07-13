from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.show_subscription_view, name='pricing_interval'),
]
