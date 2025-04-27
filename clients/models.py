from django.db import models
import uuid
from programs.models import HealthProgram

class Client(models.Model):
    """Model for clients/patients in the system"""
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    emergency_contact = models.CharField(max_length=20)
    registration_date = models.DateField(auto_now_add=True)
    programs = models.ManyToManyField(HealthProgram, through='Enrollment', related_name='clients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_active_programs(self):
        """Return all active programs the client is enrolled in"""
        return self.programs.filter(enrollment__status='active')
    
    class Meta:
        ordering = ['-registration_date']

class Enrollment(models.Model):
    """Model for client enrollment in health programs"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.client} - {self.program}"
    
    class Meta:
        unique_together = ('client', 'program')
        ordering = ['-enrollment_date']