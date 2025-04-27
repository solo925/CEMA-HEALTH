from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        """Test creating a new user"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
            first_name='Admin',
            last_name='User'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_email_normalization(self):
        """Test email is normalized when creating a user"""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, email.lower())

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', 
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')

    def test_login_page_loads(self):
        """Test that the login page loads correctly"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_successful(self):
        """Test login is successful with correct credentials"""
        response = self.client.post(
            self.login_url, 
            {'username': 'test@example.com', 'password': 'testpassword123'}
        )
        self.assertRedirects(response, self.dashboard_url)
        
        # Test we are logged in
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)

    def test_login_failed(self):
        """Test login fails with wrong credentials"""
        response = self.client.post(
            self.login_url, 
            {'username': 'test@example.com', 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'form', None, 'Please enter a correct email and password. Note that both fields may be case-sensitive.')

class RegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_page_loads(self):
        """Test that the register page loads correctly"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_successful(self):
        """Test registration is successful with valid data"""
        response = self.client.post(
            self.register_url, 
            {
                'email': 'newuser@example.com',
                'first_name': 'New',
                'last_name': 'User',
                'password1': 'newpassword123',
                'password2': 'newpassword123',
            }
        )
        self.assertRedirects(response, self.login_url)
        
        # Check user was created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        response = self.client.post(
            self.register_url, 
            {
                'email': 'newuser@example.com',
                'first_name': 'New',
                'last_name': 'User',
                'password1': 'newpassword123',
                'password2': 'differentpassword',
            }
        )
        self.assertEqual(response.status_code, 200) 
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")
        
        # Check user was not created
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())