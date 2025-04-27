import unittest
from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model
from ..forms import LoginForm, RegisterForm

User = get_user_model()

class AuthFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_form_fields(self):
        form = LoginForm()
        self.assertIsInstance(form.fields['username'], forms.EmailField)
        self.assertIsInstance(form.fields['password'], forms.CharField)
        
        # Verify widget attributes
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'form-control')

    def test_login_valid_credentials(self):
        form = LoginForm(data={
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_login_invalid_credentials(self):
        form = LoginForm(data={
            'username': 'wrong@example.com',
            'password': 'wrongpass'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Please enter a correct email address and password', form.errors['__all__'][0])

    def test_register_form_fields(self):
        form = RegisterForm()
        self.assertIsInstance(form.fields['email'], forms.EmailField)
        self.assertIsInstance(form.fields['first_name'], forms.CharField)
        self.assertIsInstance(form.fields['last_name'], forms.CharField)
        
        # Verify widget attributes
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Password')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Confirm Password')

    def test_password_mismatch(self):
        form = RegisterForm(data={
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'differentpass'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("The two password fields didn't match.", form.errors['password2'][0])

    def test_user_creation(self):
        form = RegisterForm(data={
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'new@example.com')
        self.assertEqual(user.get_full_name(), 'New User')

    def test_register_form_meta(self):
        form = RegisterForm()
        self.assertEqual(form._meta.model, User)
        self.assertEqual(form._meta.fields, ['email', 'first_name', 'last_name', 'password1', 'password2'])

if __name__ == '__main__':
    unittest.main()