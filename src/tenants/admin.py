from django.contrib import admin

from .models import Tenants

class TenantAdmin(admin.ModelAdmin):
    readonly_fields=['schema_name','active_at','inactive_at','timestamp','updated']

admin.site.register(Tenants,TenantAdmin)
