from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Client
from programs.models import HealthProgram

@login_required
def dashboard(request):
    # Get counts for dashboard
    total_clients = Client.objects.count()
    active_programs = HealthProgram.objects.filter(status='active').count()
    total_programs = HealthProgram.objects.count()
    
    # Get recent clients
    recent_clients = Client.objects.all()[:5]
    
    # Get active programs
    active_programs_list = HealthProgram.objects.filter(status='active')[:5]
    
    return render(request, 'dashboard.html', {
        'total_clients': total_clients,
        'active_programs': active_programs,
        'total_programs': total_programs,
        'recent_clients': recent_clients,
        'active_programs_list': active_programs_list,
    })