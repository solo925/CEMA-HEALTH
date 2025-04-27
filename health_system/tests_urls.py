from django.test import SimpleTestCase
from django.urls import reverse, resolve
from health_system.views import dashboard
from accounts.views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView
from clients.views import (
    client_list, client_detail, client_create, 
    client_update, client_enroll
)
from programs.views import (
    program_list, program_detail, program_create, 
    program_update
)

class UrlsTest(SimpleTestCase):
    """Test URL configuration"""
    
    def test_dashboard_url(self):
        url = reverse('dashboard')
        self.assertEqual(url, '/')
        self.assertEqual(resolve(url).func, dashboard)
    
    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(url, '/login/')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)
    
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(url, '/logout/')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
    
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(url, '/register/')
        self.assertEqual(resolve(url).func.view_class, RegisterView)
    
    def test_client_urls(self):
        # Client list
        url = reverse('client_list')
        self.assertEqual(url, '/clients/')
        self.assertEqual(resolve(url).func, client_list)
        
        # Client create
        url = reverse('client_create')
        self.assertEqual(url, '/clients/create/')
        self.assertEqual(resolve(url).func, client_create)
        
        # Client detail
        client_id = 'f47ac10b-58cc-4372-a567-0e02b2c3d479'  # Sample UUID
        url = reverse('client_detail', args=[client_id])
        self.assertEqual(url, f'/clients/{client_id}/')
        self.assertEqual(resolve(url).func, client_detail)
        
        # Client update
        url = reverse('client_update', args=[client_id])
        self.assertEqual(url, f'/clients/{client_id}/update/')
        self.assertEqual(resolve(url).func, client_update)
        
        # Client enroll
        url = reverse('client_enroll', args=[client_id])
        self.assertEqual(url, f'/clients/{client_id}/enroll/')
        self.assertEqual(resolve(url).func, client_enroll)
    
    def test_program_urls(self):
        # Program list
        url = reverse('program_list')
        self.assertEqual(url, '/programs/')
        self.assertEqual(resolve(url).func, program_list)
        
        # Program create
        url = reverse('program_create')
        self.assertEqual(url, '/programs/create/')
        self.assertEqual(resolve(url).func, program_create)
        
        # Program detail
        program_id = 'f47ac10b-58cc-4372-a567-0e02b2c3d479'  # Sample UUID
        url = reverse('program_detail', args=[program_id])
        self.assertEqual(url, f'/programs/{program_id}/')
        self.assertEqual(resolve(url).func, program_detail)
        
        # Program update
        url = reverse('program_update', args=[program_id])
        self.assertEqual(url, f'/programs/{program_id}/update/')
        self.assertEqual(resolve(url).func, program_update)