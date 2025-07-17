from typing import Any
from django.apps import apps
from django.db import connection
from django.core.management.base import BaseCommand
from django.core.management import call_command
from helpers.db import statements as db_statements
from django.contrib.auth import get_user_model
from django.conf import settings
CONSTUMER_INSTALLED_APPS=getattr(settings,'CONSTUMER_INSTALLED_APPS',[])#Handels if the constumer installed app is empty 

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        tenant_schemas = ['example',]  # put your schemas here
        with connection.cursor() as cursor:
                cursor.execute(
                    db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name="public")
                )
                call_command("migrate", interactive=False)
        for schema_name in tenant_schemas:
            self.stdout.write(f"Activating schema: {schema_name}")
            with connection.cursor() as cursor:
                cursor.execute(
                    db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name)
                )
                self.stdout.write(f"Running migrations on schema: {schema_name}")
                for app in apps.get_app_configs():
                    if app.label in CONSTUMER_INSTALLED_APPS:
                        try:

                            call_command("migrate",label=app.label, interactive=False)
                        except Exception as e:
                            self.stdout.write(f"There is no migrations in : {app.label}")
            user = get_user_model()
            if not user.objects.filter(username="Test").exists():
                self.stdout.write(f"Creating superuser on schema: {schema_name}")
                user.objects.create_superuser(
                    username="Test",
                    password="123@xenon"
                )
            else:
                self.stdout.write(f"Superuser already exists in schema: {schema_name}")
