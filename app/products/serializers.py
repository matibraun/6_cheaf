from alerts.serializers import AlertSerializer
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=2000)
    stock_quantity = serializers.IntegerField()
    expiration_date = serializers.DateField()
    alerts = AlertSerializer(many=True, read_only=True)

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        return Product.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.stock_quantity = validated_data.get('stock_quantity', instance.stock_quantity)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        
        instance.save()
        return instance