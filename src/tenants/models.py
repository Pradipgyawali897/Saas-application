from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from helpers.db.validators import validate_block_subdomain,validate_subdomain
from  .utils import geerate_unique_schema_name

class Tenants(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,db_index=True,editable=False)
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    subdomain=models.CharField(max_length=60,unique=True,
                                validators=[validate_subdomain,validate_block_subdomain])
    schema_name=models.CharField(max_length=60,unique=True,blank=True,null=True)
    active=models.BooleanField(default=True)
    active_at=models.DateTimeField(null=True,blank=True)
    inactive_at=models.DateTimeField(null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def save(self,*args, **kwargs):
        now=timezone.now()
        if self.active and not self.active_at:
            self.active_at=now
            self.inactive_at=None
        elif not self.active and not self.inactive_at:
            self.inactive_at=now
            self.active_at=None
        if not self.schema_name:
            self.schema_name=geerate_unique_schema_name(tenant_id=self.id)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.owner.username
    
