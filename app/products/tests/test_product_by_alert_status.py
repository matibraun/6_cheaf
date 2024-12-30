from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product
from alerts.models import Alert
from datetime import date, timedelta

class ProductsByAlertStatusAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            expiration_date=date.today() + timedelta(days=5),
            stock_quantity=100,
            user=self.user
        )
        Alert.objects.create(product=product, days_before_expiration_to_trigger=5)

    def test_filter_products_by_alert_status(self):
        response = self.client.get("/products/filter-by-alert-status/?status=active")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)
