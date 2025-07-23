from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.apps import apps
from contextlib import contextmanager

User = get_user_model()

DEFAULT_USER_EMAIL = "admin@tenant.com"
DEFAULT_USER_PASSWORD = "admin123"
DEFAULT_USER_FIRST_NAME = "Admin"
DEFAULT_USER_LAST_NAME = "User"

Tenant = apps.get_model("tenants", "Tenants")


@contextmanager
def schema_context(schema_name):
    """Temporarily switch to a given schema."""
    with connection.cursor() as cursor:
        original_search_path = connection.settings_dict.get('search_path', 'public')
        cursor.execute(f'SET search_path TO {schema_name}, public')
        try:
            yield
        finally:
            cursor.execute(f'SET search_path TO {original_search_path}')


class Command(BaseCommand):
    help = "Create a default superuser in each active tenant schema (no arguments required)."

    def handle(self, *args, **options):
        for tenant_obj in Tenant.objects.filter(active=True):
            schema_name = tenant_obj.schema_name
            self.stdout.write(f"🔍 Checking schema: {schema_name}")

            with schema_context(schema_name):
                if not User.objects.filter(email=DEFAULT_USER_EMAIL).exists():
                    User.objects.create_user(
                        username="admin",
                        email=DEFAULT_USER_EMAIL,
                        password=DEFAULT_USER_PASSWORD,
                        first_name=DEFAULT_USER_FIRST_NAME,
                        last_name=DEFAULT_USER_LAST_NAME,
                        is_staff=True,
                        is_superuser=True,
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"✅ Created default user for tenant '{schema_name}'"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ Default user already exists in schema '{schema_name}'"
                    ))
