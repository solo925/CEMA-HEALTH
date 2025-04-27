import unittest
from django import forms
from django.test import TestCase
from unittest.mock import patch
from .models import Client, Enrollment
from ..forms import ClientForm, EnrollmentForm

class FormsTestCase(TestCase):
    def test_client_form_fields(self):
        form = ClientForm()
        self.assertEqual(list(form.fields), ['first_name', 'last_name', 'date_of_birth', 'gender', 
                                             'contact_number', 'email', 'address', 'emergency_contact'])
        
        # Verify widget attributes
        self.assertIsInstance(form.fields['date_of_birth'].widget, forms.DateInput)
        self.assertEqual(form.fields['date_of_birth'].widget.attrs['type'], 'date')
        self.assertIsInstance(form.fields['address'].widget, forms.Textarea)
        self.assertEqual(form.fields['address'].widget.attrs['rows'], 3)

    def test_enrollment_form_fields(self):
        form = EnrollmentForm()
        self.assertEqual(list(form.fields), ['program', 'status', 'notes'])
        
        # Verify widget attributes
        self.assertIsInstance(form.fields['notes'].widget, forms.Textarea)
        self.assertEqual(form.fields['notes'].widget.attrs['rows'], 3)

    @patch('django.db.models.Model.save', autospec=True)
    def test_client_form_valid_data(self, mock_save):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'contact_number': '1234567890',
            'email': 'john.doe@example.com',
            'address': '123 Main St',
            'emergency_contact': 'Jane Doe'
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(mock_save.called)

    @patch('django.db.models.Model.save', autospec=True)
    def test_enrollment_form_valid_data(self, mock_save):
        form_data = {
            'program': 'Yoga',
            'status': 'Active',
            'notes': 'Enrolled for morning sessions'
        }
        form = EnrollmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(mock_save.called)

    def test_client_form_invalid_data(self):
        form_data = {
            'first_name': '',
            'last_name': '',
            'date_of_birth': '',
            'gender': '',
            'contact_number': '',
            'email': 'invalid-email',
            'address': '',
            'emergency_contact': ''
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('email', form.errors)

    def test_enrollment_form_invalid_data(self):
        form_data = {
            'program': '',
            'status': '',
            'notes': ''
        }
        form = EnrollmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('program', form.errors)

if __name__ == '__main__':
    unittest.main()
