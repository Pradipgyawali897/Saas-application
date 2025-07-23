from helpers.db import schemas
from django.apps import apps
from django.core.cache import cache

class SchemaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host_split = request.get_host().split(":")[0].split(".")
        subdomain = None
        if len(host_split) > 1:
            subdomain = host_split[0]

        schema_name = self.get_schema_name(subdomain=subdomain)
        schemas.activate_tenant_schema(schema_name=schema_name)
        return self.get_response(request)

    def get_schema_name(self, subdomain=None):
        if subdomain is None or subdomain == "localhost":
            return "public"

        cache_key = f"subdomain_schema:{subdomain}"
        cache_value = cache.get(cache_key)
        if cache_value:
            return cache_value

        with schemas.use_public_schema():
            Tenant = apps.get_model("tenants", "Tenants")
            try:
                obj = Tenant.objects.get(subdomain=subdomain)
                schema_name = obj.schema_name
                cache.set(cache_key, schema_name, 60) 
            except Tenant.DoesNotExist:
                print(f"Subdomain '{subdomain}' not found.")
                schema_name = "public"
                cache.set(cache_key, schema_name, 60)  
            except Exception as e:
                print(f"{e} Exception arrived in middleware")
                schema_name = "public" 
        return schema_name
