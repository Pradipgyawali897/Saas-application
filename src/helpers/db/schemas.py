from helpers.db import statements
from django.db import connection
from contextlib import contextmanager
DEFAULT_SCHEMA="public"



def check_schema_exists(schema_name,required_check=False):
    if schema_name==DEFAULT_SCHEMA and not required_check:
        return True
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = %s
        """, [schema_name])
        return bool(cursor.fetchone())


def activate_tenant_schema(schema_name=None):
    is_exists=check_schema_exists(schema_name)
    schema_to_use=DEFAULT_SCHEMA
    if is_exists :
        schema_to_use=schema_name
        with connection.cursor() as cursor:
                cursor.execute(
                    statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_to_use)   
                )
                connection.schema_name=schema_to_use

@contextmanager
def use_public_schema(revert_schema_name=None, revert_schema=False):
    """
    with use_public_schema():
        Tenant.object.all()
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                statements.ACTIVATE_SCHEMA_SQL.format(schema_name=DEFAULT_SCHEMA)   
            )
            yield
    finally:
        if revert_schema:
            activate_tenant_schema(revert_schema_name)


    