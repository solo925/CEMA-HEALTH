import unittest
from django import forms
from django.test import TestCase
from unittest.mock import patch
from .models import HealthProgram
from ..forms import ProgramForm

class ProgramFormTestCase(TestCase):
    def test_program_form_fields(self):
        form = ProgramForm()
        self.assertEqual(list(form.fields), ['name', 'description', 'start_date', 'end_date', 'status', 'capacity'])
        
        # Verify widget attributes
        self.assertIsInstance(form.fields['start_date'].widget, forms.DateInput)
        self.assertEqual(form.fields['start_date'].widget.attrs['type'], 'date')
        self.assertIsInstance(form.fields['end_date'].widget, forms.DateInput)
        self.assertEqual(form.fields['end_date'].widget.attrs['type'], 'date')
        self.assertIsInstance(form.fields['description'].widget, forms.Textarea)
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 4)

    @patch('django.db.models.Model.save', autospec=True)
    def test_program_form_valid_data(self, mock_save):
        form_data = {
            'name': 'Yoga Retreat',
            'description': 'A relaxing yoga retreat.',
            'start_date': '2023-11-01',
            'end_date': '2023-11-10',
            'status': 'Open',
            'capacity': 20
        }
        form = ProgramForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(mock_save.called)

    def test_program_form_invalid_data(self):
        form_data = {
            'name': '',
            'description': '',
            'start_date': '',
            'end_date': '',
            'status': '',
            'capacity': ''
        }
        form = ProgramForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('start_date', form.errors)

if __name__ == '__main__':
    unittest.main()
