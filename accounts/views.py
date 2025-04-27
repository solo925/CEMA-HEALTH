from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import LoginForm, RegisterForm

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Add success message
        from django.contrib import messages
        messages.success(self.request, 'Registration successful! Please log in with your new account.')
        return response
