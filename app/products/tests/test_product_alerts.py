from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product
from alerts.models import Alert
from datetime import date, timedelta

class ProductAlertsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            expiration_date=date.today() + timedelta(days=10),
            stock_quantity=100,
            user=self.user
        )
        Alert.objects.create(product=self.product, days_before_expiration_to_trigger=5)

    def test_get_product_alerts(self):
        response = self.client.get(f"/products/{self.product.id}/alerts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
