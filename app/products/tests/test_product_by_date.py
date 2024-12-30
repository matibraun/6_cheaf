from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product
from alerts.models import Alert
from datetime import date, timedelta

class ProductsByDateAPITestCase(APITestCase):

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
        Product.objects.create(
            name="Product 2",
            description="Description 2",
            expiration_date=date.today() + timedelta(days=10),
            stock_quantity=30,
            user=self.user
        )

    def test_filter_products_by_dates(self):
        start_date = date.today().isoformat()
        end_date = (date.today() + timedelta(days=7)).isoformat()
        response = self.client.get(f"/products/filter-by-dates/?start_date={start_date}&end_date={end_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
