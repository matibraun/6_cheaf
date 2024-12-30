from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegisterUserViewTests(APITestCase):
    def test_register_user_successful(self):
        payload = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/users/register/', payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertNotIn('password', response.data)  # Password should not be in the response

        # Check user creation
        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('password123'))

    def test_register_user_invalid_data(self):
        payload = {
            'username': '',  # Empty username
            'password': 'password123',
            'email': 'invalid-email',  # Invalid email format
        }
        response = self.client.post('/users/register/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
