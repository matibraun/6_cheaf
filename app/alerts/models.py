from django.db import models

from products.models import Product

class Alert(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    days_before_expiration_to_trigger = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)