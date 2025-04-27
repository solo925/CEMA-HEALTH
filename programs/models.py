from django.db import models
import uuid

class HealthProgram(models.Model):
    """Model for health programs like TB, Malaria, HIV, etc."""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    capacity = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def enrolled_count(self):
        """Return the number of clients enrolled in this program"""
        return self.enrollments.count()
    
    class Meta:
        ordering = ['-start_date']
