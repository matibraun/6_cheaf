from django.db import models
from datetime import date
from django.db.models import F
from django.contrib.auth.models import User

class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    stock_quantity = models.IntegerField()
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_products_with_active_alerts(cls):
        today = date.today()
        return cls.objects.filter(
            expiration_date__gt=F('alerts__days_before_expiration_to_trigger') + today
        ).distinct().prefetch_related('alerts')
    
    @classmethod
    def get_products_with_alerts_to_be_triggered_today(cls):
        today = date.today()
        return cls.objects.filter(
            expiration_date=F('alerts__days_before_expiration_to_trigger') + today
        ).select_related('user').prefetch_related('alerts')