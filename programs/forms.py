from django import forms
from .models import HealthProgram

class ProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'capacity']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }