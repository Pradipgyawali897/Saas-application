from django.core.management.base import BaseCommand
from django.db import connection
from helpers.db import statements
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        schema_name="costumer_a"
        with connection.cursor() as cursor:
            cursor.execute(statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name))