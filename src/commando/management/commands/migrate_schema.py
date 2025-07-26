from helpers.db import statements as db_statements
from helpers.db.schemas import check_schema_exists, activate_tenant_schema, use_public_schema 
from django.db import connection
from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.conf import settings
from django.db.migrations.executor import MigrationExecutor
import re

DEFAULT_SCHEMA = "public"

def is_valid_schema_name(name: str) -> bool:
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

class Command(BaseCommand):

    def handle(self, *args, **options):
        Tenant = apps.get_model("tenants", "Tenants")

        if not is_valid_schema_name(DEFAULT_SCHEMA):
            self.stderr.write("Error: Invalid schema name 'public'.")
            return

        if not check_schema_exists(DEFAULT_SCHEMA, required_check=True):
            with connection.cursor() as cursor:
                cursor.execute(
                    db_statements.CREATE_SCHEMA_SQL.format(schema_name=DEFAULT_SCHEMA)
                )

        skip_public = False

        if not skip_public:
            with use_public_schema():
                call_command("migrate", interactive=False)

        # Run migrations for each tenant
        for tenant_obj in Tenant.objects.filter(active=True):
            schema_name = tenant_obj.schema_name

            if not is_valid_schema_name(schema_name):
                self.stderr.write(f"Error: Invalid schema name '{schema_name}'. Skipping.")
                continue

            if not check_schema_exists(schema_name):
                with connection.cursor() as cursor:
                    cursor.execute(
                        db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
                    )
                self.stdout.write(self.style.SUCCESS(f"Created schema '{schema_name}'"))

            activate_tenant_schema(schema_name)

            executor = MigrationExecutor(connection)
            loader = executor.loader
            loader.build_graph()

            customer_apps = getattr(settings, 'CUSTOMER_INSTALLED_APPS', [])
            customer_app_configs = [
                app_config for app_config in apps.get_app_configs()
                if app_config.name in customer_apps
            ]

            for app_config in customer_app_configs:
                app_label = app_config.label
                leaf_nodes = [
                    node for node in loader.graph.leaf_nodes()
                    if node[0] == app_label
                ]

                if not leaf_nodes:
                    continue

                full_plan = []
                for leaf in leaf_nodes:
                    plan = executor.migration_plan([leaf])
                    for migration, backwards in plan:
                        if not backwards:
                            full_plan.append(migration)

                seen = set()
                ordered_migrations = []
                for m in full_plan:
                    if m not in seen:
                        seen.add(m)
                        ordered_migrations.append(m)

                if not ordered_migrations:
                    continue

                self.stdout.write(f"Applying migrations for '{app_label}':")
                for migration in ordered_migrations:
                    self.stdout.write(f"  - {migration.app_label}.{migration.name}")

                executor.migrate(leaf_nodes)
                executor.loader.build_graph()

            self.stdout.write(self.style.SUCCESS("All migrations for CUSTOMER_APPS are completed."))
