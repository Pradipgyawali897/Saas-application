import re
from typing import Any
from django.db import connection
from django.core.management.base import BaseCommand

from helpers.db import statements as db_statements

def is_valid_schema_name(name: str) -> bool:
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, nargs='?', default=None)

    def handle(self, *args: Any, **options: Any):
        schema_name = options.get('schema_name')

        if not schema_name:
            self.stderr.write("Error: Please provide a schema name.")
            return

        if not is_valid_schema_name(schema_name):
            self.stderr.write("Error: Invalid schema name. Use only letters, digits, and underscores. It must start with a letter or underscore.")
            return

        with connection.cursor() as cursor:
            cursor.execute(
                db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
            )
            cursor.execute(
                db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name)
            )

        self.stdout.write(self.style.SUCCESS(f"Schema '{schema_name}' created and activated."))
