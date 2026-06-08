
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        modal=Product
        fields=['id','name','sku','price']