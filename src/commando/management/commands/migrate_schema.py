import re
from typing import Any

from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.db import connection
from django.conf import settings
from django.db.migrations.executor import MigrationExecutor

from helpers.db import statements as db_statements

def is_valid_schema_name(name: str) -> bool:
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        Tenant = apps.get_model("tenants", "Tenants")

        # Validate "public" schema
        if not is_valid_schema_name("public"):
            self.stderr.write("Error: Invalid schema name 'public'.")
            return

        with connection.cursor() as cursor:
            cursor.execute(
                db_statements.CREATE_SCHEMA_SQL.format(schema_name="public")
            )
            cursor.execute(
                db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name="public")
            )

        qs = Tenant.objects.filter(active=True)
        skip_public = True

        if not skip_public:
            call_command("migrate", interactive=False)

        for tenant_obj in qs:
            schema_name = tenant_obj.schema_name

            if not is_valid_schema_name(schema_name):
                self.stderr.write(f"Error: Invalid schema name '{schema_name}'. Skipping.")
                continue

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = %s
                """, [schema_name])
                schema_exists = bool(cursor.fetchone())

                if not schema_exists:
                    cursor.execute(
                        db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created schema '{schema_name}'"))

                cursor.execute(db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name))

            executor = MigrationExecutor(connection)
            loader = executor.loader
            loader.build_graph()

            customer_apps = getattr(settings, 'CONSTUMER_INSTALLED_APPS', [])
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
