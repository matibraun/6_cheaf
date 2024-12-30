from rest_framework.test import APITestCase
from rest_framework import status
from alerts.models import Alert
from products.models import Product
from django.contrib.auth.models import User
from datetime import date, timedelta

class AlertsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

        self.client.login(username='testuser', password='password123')

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            expiration_date=date.today() + timedelta(days=10),
            stock_quantity=100,
            user=self.user
        )

        self.alert1 = Alert.objects.create(
            product=self.product,
            days_before_expiration_to_trigger=5
        )
        self.alert2 = Alert.objects.create(
            product=self.product,
            days_before_expiration_to_trigger=10
        )

    def test_create_alert(self):
        payload = {
            "product_id": self.product.id,
            "days_before_expiration_to_trigger": 7
        }
        response = self.client.post('/alerts/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['days_before_expiration_to_trigger'], 7)

    def test_get_all_alerts(self):
        response = self.client.get('/alerts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        total_alerts = Alert.objects.count()
        self.assertEqual(len(response.data), total_alerts)

    def test_get_single_alert(self):
        response = self.client.get(f'/alerts/{self.alert1.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.alert1.id)

    def test_update_alert(self):
        payload = {"days_before_expiration_to_trigger": 15}
        response = self.client.patch(f'/alerts/{self.alert1.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.alert1.refresh_from_db()
        self.assertEqual(self.alert1.days_before_expiration_to_trigger, 15)

    def test_delete_alert(self):
        response = self.client.delete(f'/alerts/{self.alert1.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Alert.objects.filter(id=self.alert1.id).exists())

    def test_filter_alerts_by_status_active(self):
        response = self.client.get('/alerts/filter-by-status/?status=active', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_alerts_by_status_expired(self):
        self.product.expiration_date = date.today() - timedelta(days=1)
        self.product.save()

        response = self.client.get('/alerts/filter-by-status/?status=expired', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_alerts_by_invalid_status(self):
        response = self.client.get('/alerts/filter-by-status/?status=invalid', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
