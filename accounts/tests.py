"""
Tests for the accounts app.

This module contains tests for authentication functionality including:
- User registration and login
- UserProfile model functionality
- Authentication views
- URL routing
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import UserProfile


class UserProfileModelTest(TestCase):
    """Test cases for the UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test that UserProfile is created automatically when User is created."""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertIsInstance(self.user.userprofile, UserProfile)
    
    def test_user_profile_str_method(self):
        """Test the string representation of UserProfile."""
        expected = f"{self.user.username}'s Profile"
        self.assertEqual(str(self.user.userprofile), expected)
    
    def test_user_profile_fields(self):
        """Test UserProfile model fields."""
        profile = self.user.userprofile
        
        # Test default values
        self.assertEqual(profile.bio, '')
        self.assertFalse(profile.avatar)
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
    
    def test_user_profile_update(self):
        """Test updating UserProfile fields."""
        profile = self.user.userprofile
        profile.bio = 'This is a test bio'
        profile.save()
        
        # Refresh from database
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'This is a test bio')


class AuthenticationViewsTest(TestCase):
    """Test cases for authentication views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_view_get(self):
        """Test GET request to registration view."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertContains(response, 'form')
    
    def test_register_view_post_valid(self):
        """Test POST request to registration view with valid data."""
        data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('accounts:register'), data)
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check UserProfile was created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'userprofile'))
    
    def test_register_view_post_invalid(self):
        """Test POST request to registration view with invalid data."""
        data = {
            'username': 'newuser',
            'password1': 'pass',
            'password2': 'different'
        }
        response = self.client.post(reverse('accounts:register'), data)
        
        # Should stay on registration page with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
        
        # Check user was not created
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_login_view_get(self):
        """Test GET request to login view."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'form')
    
    def test_login_view_post_valid(self):
        """Test POST request to login view with valid credentials."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('accounts:login'), data)
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:dashboard'))
    
    def test_login_view_post_invalid(self):
        """Test POST request to login view with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('accounts:login'), data)
        
        # Should stay on login page with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
    
    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'testuser')
    
    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view for unauthenticated user."""
        response = self.client.get(reverse('accounts:dashboard'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}")
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'testuser')
    
    def test_profile_view_unauthenticated(self):
        """Test profile view for unauthenticated user."""
        response = self.client.get(reverse('accounts:profile'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")
    
    def test_profile_update_post(self):
        """Test updating profile via POST request."""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'bio': 'Updated bio content'
        }
        response = self.client.post(reverse('accounts:profile'), data)
        
        # Should redirect after successful update
        self.assertEqual(response.status_code, 302)
        
        # Check profile was updated
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.bio, 'Updated bio content')
    
    def test_logout_functionality(self):
        """Test logout functionality."""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Verify user is logged in
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Logout
        response = self.client.post(reverse('accounts:logout'))
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        
        # Verify user is logged out
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login


class URLRoutingTest(TestCase):
    """Test cases for URL routing."""
    
    def test_accounts_urls_resolve(self):
        """Test that all accounts URLs resolve correctly."""
        urls_to_test = [
            'accounts:register',
            'accounts:login',
            'accounts:logout',
            'accounts:dashboard',
            'accounts:profile',
            'accounts:password_change',
            'accounts:password_change_done',
        ]
        
        for url_name in urls_to_test:
            with self.subTest(url_name=url_name):
                url = reverse(url_name)
                self.assertIsNotNone(url)
                self.assertTrue(url.startswith('/accounts/'))


class AuthenticationIntegrationTest(TestCase):
    """Integration tests for the complete authentication flow."""
    
    def test_complete_registration_login_flow(self):
        """Test complete user registration and login flow."""
        # Step 1: Register a new user
        registration_data = {
            'username': 'integrationuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('accounts:register'), registration_data)
        self.assertEqual(response.status_code, 302)
        
        # Step 2: Verify user and profile were created
        user = User.objects.get(username='integrationuser')
        self.assertTrue(hasattr(user, 'userprofile'))
        
        # Step 3: Login with the new user
        login_data = {
            'username': 'integrationuser',
            'password': 'complexpass123'
        }
        response = self.client.post(reverse('accounts:login'), login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:dashboard'))
        
        # Step 4: Access protected pages
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'integrationuser')
        
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        
        # Step 5: Update profile
        profile_data = {
            'bio': 'Integration test bio'
        }
        response = self.client.post(reverse('accounts:profile'), profile_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify profile update
        user.userprofile.refresh_from_db()
        self.assertEqual(user.userprofile.bio, 'Integration test bio')
        
        # Step 6: Logout
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        
        # Step 7: Verify logout worked
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
