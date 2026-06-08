from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    # Force READ operations to only fetch data belonging to the authenticated tenant
    def get_queryset(self):
        tenant = self.request.tenant
        return Product.objects.filter(tenant=tenant)

    # Automatically attach the tenant context on WRITE operations
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)