import hashlib


def geerate_unique_schema_name(tenant_id:str):
    base_name=f"tenant_{tenant_id}"
    base_name=base_name.replace("-","")
    hash_suffix=hashlib.sha256(base_name.encode("utf-8")).hexdigest()[0:16]
    unique_name=base_name[:40]
    schema_name=f"{unique_name}-{hash_suffix}"
    schema_name=schema_name.replace("-","")
    return base_name[0:60]