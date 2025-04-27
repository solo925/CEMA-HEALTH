from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import HealthProgram
from clients.models import Client, Enrollment
from datetime import date, timedelta

User = get_user_model()

class HealthProgramModelTest(TestCase):
    def test_create_program(self):
        """Test creating a health program"""
        program = HealthProgram.objects.create(
            name='Test Program',
            description='Test program description',
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            status='active',
            capacity=50
        )
        self.assertEqual(program.name, 'Test Program')
        self.assertEqual(program.description, 'Test program description')
        self.assertEqual(program.status, 'active')
        self.assertEqual(program.capacity, 50)
        self.assertEqual(str(program), 'Test Program')
    
    def test_enrolled_count_property(self):
        """Test the enrolled_count property on HealthProgram"""
        program = HealthProgram.objects.create(
            name='Test Program',
            description='Test program description',
            start_date=date(2023, 1, 1),
            status='active'
        )
        
        # Create clients and enroll them
        client1 = Client.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            gender='male',
            contact_number='1234567890',
            email='john@example.com',
            address='123 Test St',
            emergency_contact='0987654321'
        )
        
        client2 = Client.objects.create(
            first_name='Jane',
            last_name='Smith',
            date_of_birth=date(1992, 5, 15),
            gender='female',
            contact_number='9876543210',
            email='jane@example.com',
            address='456 Test Ave',
            emergency_contact='1234567890'
        )
        
        # Create enrollments
        Enrollment.objects.create(client=client1, program=program, status='active')
        Enrollment.objects.create(client=client2, program=program, status='active')
        
        # Test the enrolled_count property
        self.assertEqual(program.enrolled_count, 2)

class ProgramViewsTest(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Create a program
        self.program = HealthProgram.objects.create(
            name='Test Program',
            description='Test program description',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
            status='active',
            capacity=50
        )
        
        # URLs
        self.program_list_url = reverse('program_list')
        self.program_detail_url = reverse('program_detail', args=[self.program.id])
        self.program_create_url = reverse('program_create')
        self.program_update_url = reverse('program_update', args=[self.program.id])
        
        # Login
        self.client.login(username='test@example.com', password='testpassword123')

    def test_program_list_view(self):
        """Test the program list view"""
        response = self.client.get(self.program_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programs/program_list.html')
        self.assertContains(response, 'Test Program')

    def test_program_detail_view(self):
        """Test the program detail view"""
        response = self.client.get(self.program_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programs/program_detail.html')
        self.assertContains(response, 'Test Program')
        self.assertContains(response, 'Test program description')

    def test_program_create_view(self):
        """Test the program create view"""
        response = self.client.get(self.program_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programs/program_form.html')
        
        # Test POST with valid data
        program_data = {
            'name': 'New Program',
            'description': 'New program description',
            'start_date': date.today().strftime('%Y-%m-%d'),
            'end_date': (date.today() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'status': 'planned',
            'capacity': 100
        }
        response = self.client.post(self.program_create_url, program_data)
        
        # Should create a new program and redirect
        self.assertEqual(HealthProgram.objects.count(), 2)
        new_program = HealthProgram.objects.get(name='New Program')
        self.assertRedirects(response, reverse('program_detail', args=[new_program.id]))

    def test_program_update_view(self):
        """Test the program update view"""
        response = self.client.get(self.program_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'programs/program_form.html')
        
        # Test POST with updated data
        updated_data = {
            'name': 'Updated Program',
            'description': 'Updated description',
            'start_date': self.program.start_date.strftime('%Y-%m-%d'),
            'end_date': self.program.end_date.strftime('%Y-%m-%d'),
            'status': 'completed',
            'capacity': 75
        }
        response = self.client.post(self.program_update_url, updated_data)
        
        # Should update the program and redirect
        self.assertRedirects(response, self.program_detail_url)
        self.program.refresh_from_db()
        self.assertEqual(self.program.name, 'Updated Program')
        self.assertEqual(self.program.description, 'Updated description')
        self.assertEqual(self.program.status, 'completed')
        self.assertEqual(self.program.capacity, 75)

    def test_filter_by_status(self):
        """Test filtering programs by status"""
        # Create another program with different status
        HealthProgram.objects.create(
            name='Planned Program',
            description='Planned program description',
            start_date=date.today() + timedelta(days=30),
            status='planned'
        )
        
        # Test filtering by active status
        response = self.client.get(f"{self.program_list_url}?status=active")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Program')
        self.assertNotContains(response, 'Planned Program')
        
        # Test filtering by planned status
        response = self.client.get(f"{self.program_list_url}?status=planned")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Planned Program')
        self.assertNotContains(response, 'Test Program')