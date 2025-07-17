
from django.db import connection
from contextlib import contextmanager
DEFAULT_SCHEMA="public"
@contextmanager
def use_public_schema():
    """
    with use_public_schema():
        Tenant.object.all()
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = %s
            """, [DEFAULT_SCHEMA])
            yield
    finally:
        print("someting")

    