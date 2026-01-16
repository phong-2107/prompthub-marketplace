"""
Test suite for API endpoints.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class APITests(TestCase):
    """Tests for API endpoints."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user(self):
        """Test user creation via API."""
        payload = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        response = self.client.post('/api/users/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check user was created
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)
    
    def test_get_user_profile_authenticated(self):
        """Test getting user profile when authenticated."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_get_user_profile_unauthenticated(self):
        """Test getting user profile when not authenticated."""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.patch('/api/users/update_profile/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check user was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
