from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

class CustomLoginViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )

    def test_login_successful(self):
        payload = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post('/users/login/', payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

        # Check if the token is created
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)

    def test_login_invalid_credentials(self):
        payload = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post('/users/login/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')


