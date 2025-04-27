from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Client, Enrollment
from .forms import ClientForm, EnrollmentForm
from programs.models import HealthProgram

@login_required
def client_list(request):
    clients = Client.objects.all()
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(contact_number__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clients/client_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    enrollments = client.enrollments.all().select_related('program')
    
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'enrollments': enrollments,
    })

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            full_name = f"{client.first_name} {client.last_name}"  # Concatenate first and last names
            messages.success(request, f'Client {full_name} created successfully.')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    
    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Create Client',
    })


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.get_full_name()} updated successfully.')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'clients/client_form.html', {
        'form': form,
        'client': client,
        'title': 'Update Client',
    })

@login_required
def client_enroll(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    # Find programs client is not enrolled in
    enrolled_program_ids = client.enrollments.values_list('program_id', flat=True)
    available_programs = HealthProgram.objects.exclude(id__in=enrolled_program_ids)
    
    if request.method == 'POST':
        program_id = request.POST.get('program')
        if not program_id:
            messages.error(request, 'You must select a program.')
            return redirect('client_enroll', pk=client.pk)
        
        program = get_object_or_404(HealthProgram, pk=program_id)
        
        # Check if already enrolled
        if Enrollment.objects.filter(client=client, program=program).exists():
            messages.error(request, f'Client is already enrolled in {program.name}.')
            return redirect('client_detail', pk=client.pk)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            client=client,
            program=program,
            status='active'
        )
        
        messages.success(request, f'Client successfully enrolled in {program.name}.')
        return redirect('client_detail', pk=client.pk)
    
    return render(request, 'clients/client_enroll.html', {
        'client': client,
        'available_programs': available_programs,
    })
