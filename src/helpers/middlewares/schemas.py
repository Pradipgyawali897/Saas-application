from django.db import connection
from helpers.db import statements 
from helpers.db import schemas
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
        self.set_search_path(schema_name=schema_name)
        return self.get_response(request)
    
    def set_search_path(self,schema_name):
        with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = %s
                """, [schema_name])
                schema_exists = bool(cursor.fetchone())

                if not schema_exists:
                     schema_name="public"

                # Set the search_path
                cursor.execute(statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name))

        return
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

        