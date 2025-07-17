import re
from django.core.exceptions import ValidationError
from helpers.db.security.blocked import BLOCKED_LIST


def validate_block_subdomain(value):
    value=value.lower()
    lowerd_blocked_list=[x.lower() for x in BLOCKED_LIST ]
    if value in lowerd_blocked_list:
        raise ValidationError( f"{value} is not a valid subdomain",
                              params={"value":value})
    
def validate_subdomain(value):
    """Validator for subdomain fields in Django models."""
    subdomain_regex = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    
    if not re.match(subdomain_regex, value):
        raise ValidationError(
            f"'{value}' is not a valid subdomain. Subdomains must start and end with an alphanumeric character and can only contain alphanumeric characters and hyphens in between.",
            params={'value': value},
        )