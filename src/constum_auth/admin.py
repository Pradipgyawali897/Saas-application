from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SaasUser
class CustomUserAdmin(UserAdmin):
    model = SaasUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        
    )
admin.site.register(SaasUser)
