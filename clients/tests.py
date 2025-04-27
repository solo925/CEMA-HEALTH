from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Client, Enrollment
from programs.models import HealthProgram
import uuid
from datetime import date

User = get_user_model()

class ClientModelTest(TestCase):
    def test_create_client(self):
        """Test creating a new client"""
        client = Client.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            gender='male',
            contact_number='1234567890',
            email='john@example.com',
            address='123 Test St',
            emergency_contact='0987654321'
        )
        self.assertEqual(client.first_name, 'John')
        self.assertEqual(client.last_name, 'Doe')
        self.assertEqual(client.email, 'john@example.com')
        self.assertEqual(str(client), 'John Doe')

class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            gender='male',
            contact_number='1234567890',
            email='john@example.com',
            address='123 Test St',
            emergency_contact='0987654321'
        )
        self.program = HealthProgram.objects.create(
            name='Test Program',
            description='Test program description',
            start_date=date(2023, 1, 1),
            status='active'
        )

    def test_enroll_client(self):
        """Test enrolling a client in a program"""
        enrollment = Enrollment.objects.create(
            client=self.client,
            program=self.program,
            status='active'
        )
        self.assertEqual(enrollment.client, self.client)
        self.assertEqual(enrollment.program, self.program)
        self.assertEqual(enrollment.status, 'active')
        self.assertEqual(str(enrollment), f'{self.client} - {self.program}')

        # Check the client is enrolled in the program
        self.assertTrue(self.client.programs.filter(id=self.program.id).exists())

class ClientViewsTest(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        # Create a client
        self.client_obj = Client.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            gender='male',
            contact_number='1234567890',
            email='john@example.com',
            address='123 Test St',
            emergency_contact='0987654321'
        )
        # Create a program
        self.program = HealthProgram.objects.create(
            name='Test Program',
            description='Test program description',
            start_date=date(2023, 1, 1),
            status='active'
        )
        
        # URLs
        self.client_list_url = reverse('client_list')
        self.client_detail_url = reverse('client_detail', args=[self.client_obj.id])
        self.client_create_url = reverse('client_create')
        self.client_update_url = reverse('client_update', args=[self.client_obj.id])
        self.client_enroll_url = reverse('client_enroll', args=[self.client_obj.id])
        
        # Login
        self.client.login(username='test@example.com', password='testpassword123')

    def test_client_list_view(self):
        """Test the client list view"""
        response = self.client.get(self.client_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/client_list.html')
        self.assertContains(response, 'John Doe')

    def test_client_detail_view(self):
        """Test the client detail view"""
        response = self.client.get(self.client_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/client_detail.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'john@example.com')

    def test_client_create_view(self):
        """Test the client create view"""
        response = self.client.get(self.client_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/client_form.html')
        
        # Test POST with valid data
        client_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1992-05-15',
            'gender': 'female',
            'contact_number': '9876543210',
            'email': 'jane@example.com',
            'address': '456 Test Ave',
            'emergency_contact': '1234567890'
        }
        response = self.client.post(self.client_create_url, client_data)
        
        # Should create a new client and redirect
        self.assertEqual(Client.objects.count(), 2)
        new_client = Client.objects.get(email='jane@example.com')
        self.assertRedirects(response, reverse('client_detail', args=[new_client.id]))

    def test_client_update_view(self):
        """Test the client update view"""
        response = self.client.get(self.client_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/client_form.html')
        
        # Test POST with updated data
        updated_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'contact_number': '5555555555',  # Updated
            'email': 'john.updated@example.com',  # Updated
            'address': '123 Test St',
            'emergency_contact': '0987654321'
        }
        response = self.client.post(self.client_update_url, updated_data)
        
        # Should update the client and redirect
        self.assertRedirects(response, self.client_detail_url)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.contact_number, '5555555555')
        self.assertEqual(self.client_obj.email, 'john.updated@example.com')

    def test_client_enroll_view(self):
        """Test the client enroll view"""
        response = self.client.get(self.client_enroll_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/client_enroll.html')
        
        # Test POST to enroll client
        enrollment_data = {
            'program': str(self.program.id)
        }
        response = self.client.post(self.client_enroll_url, enrollment_data)
        
        # Should create enrollment and redirect
        self.assertRedirects(response, self.client_detail_url)
        self.assertTrue(Enrollment.objects.filter(client=self.client_obj, program=self.program).exists())