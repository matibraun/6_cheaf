from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product
from alerts.models import Alert
from datetime import date, timedelta

class ProductsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

        self.product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "expiration_date": (date.today() + timedelta(days=10)).isoformat(),
            "stock_quantity": 100
        }
        
        self.product = Product.objects.create(
            name="Existing Product",
            description="Existing Description",
            expiration_date=date.today() + timedelta(days=5),
            stock_quantity=50,
            user=self.user
        )

    def test_create_product(self):
        response = self.client.post("/products/", self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["product"]["name"], self.product_data["name"])

    def test_get_all_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 9)

    def test_get_single_product(self):
        response = self.client.get(f"/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_update_product(self):
        update_data = {"name": "Updated Product"}
        response = self.client.patch(f"/products/{self.product.id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"]["name"], update_data["name"])

    def test_delete_product(self):
        response = self.client.delete(f"/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
