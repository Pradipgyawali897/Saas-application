from django.db import connection
from helpers.db import statements,schemas
from django.apps import apps
class SchemaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        host_split=request.get_host().split(":")[0].split(".")
        subdomain=None
        if len(host_split) >1 :
            subdomain=host_split[0]
        schema_name=self.get_schema_name(subdomain=subdomain)
        schemas.activate_tenant_schema(schema_name=schema_name)
        return self.get_response(request)
    
    def get_schema_name(self,subdomain=None):
        if subdomain is None or subdomain=="localhost":
            return "public"
        with schemas.use_public_schema():
            Tenant = apps.get_model("tenants", "Tenants")
            try:
                obj=Tenant.objects.get(subdomain=subdomain)
                schema_name=obj.schema_name
            except Exception as e:
                print(f"{e} Exception arrived in middleware")
        return schema_name

        