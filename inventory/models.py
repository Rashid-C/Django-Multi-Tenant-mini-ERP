from django.db import models
from tenants.models import TenantAwareModel

class Product(TenantAwareModel):
    name = models.CharField(max_length=255)
    sku=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
