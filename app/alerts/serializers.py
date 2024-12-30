from .selectors import get_alert_status
from rest_framework import serializers
from datetime import date, timedelta

class AlertSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    days_before_expiration_to_trigger = serializers.IntegerField()
    status = serializers.SerializerMethodField()
    days_to_trigger_date = serializers.SerializerMethodField()
    days_from_trigger_date = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def update(self, instance, validated_data):
        instance.days_before_expiration_to_trigger = validated_data.get('days_before_expiration_to_trigger', instance.days_before_expiration_to_trigger)
        
        instance.save()
        return instance

    def get_status(self, obj):

        return get_alert_status(
            product_expiration_date=obj.product.expiration_date,
            days_before_expiration_to_trigger=obj.days_before_expiration_to_trigger,
        )
   
    def get_days_to_trigger_date(self, obj):
        today = date.today()
        trigger_date = obj.product.expiration_date - timedelta(days=obj.days_before_expiration_to_trigger)
        result = (trigger_date - today).days
        return result if result >= 0 else None
   
    def get_days_from_trigger_date(self, obj):
        today = date.today()
        trigger_date = obj.product.expiration_date - timedelta(days=obj.days_before_expiration_to_trigger)
        result = (trigger_date - today).days
        return -result if result < 0 else None
