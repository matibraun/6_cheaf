from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product
from alerts.models import Alert
from datetime import date, timedelta

class ProductsByDaysAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        Product.objects.create(
            name="Product 1",
            description="Description 1",
            expiration_date=date.today() + timedelta(days=5),
            stock_quantity=50,
            user=self.user
        )

    def test_filter_products_by_days(self):
        response = self.client.get("/products/filter-by-days/?days=7")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
