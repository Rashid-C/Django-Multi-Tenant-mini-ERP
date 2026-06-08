from django.db import models


class Tenant(models.Model):
    name=models.CharField(max_length=255)
    subdommain=models.CharField(max_length=100, unique=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    # Abstract base model that other apps will inherit
class TenantAwareModel(models.Model):
    tenant=models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    class Meta:
        abstract=True
        # Tells Django not to create a separate table for this model