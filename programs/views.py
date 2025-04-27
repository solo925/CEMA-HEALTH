from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import HealthProgram
from .forms import ProgramForm
from django.db import models 

@login_required
def program_list(request):
    programs = HealthProgram.objects.all()
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        programs = programs.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'all':
        programs = programs.filter(status=status_filter)
    
    # Calculate capacity usage ratio for each program
    for program in programs:
        if program.capacity:
            program.capacity_usage_ratio = (program.enrolled_count / program.capacity) * 100
        else:
            program.capacity_usage_ratio = 0
    
    # Pagination
    paginator = Paginator(programs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'programs/program_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    })

@login_required

def program_detail(request, pk):
    program = get_object_or_404(HealthProgram, pk=pk)
    enrollments = program.enrollments.all()

    # Calculate the capacity usage ratio
    capacity_usage_ratio = 0
    if program.capacity:
        capacity_usage_ratio = (program.enrolled_count / program.capacity) * 100

    return render(request, 'programs/program_detail.html', {
        'program': program,
        'enrollments': enrollments,
        'capacity_usage_ratio': capacity_usage_ratio,
    })


@login_required
def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, f'Program {program.name} created successfully.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = ProgramForm()
    
    return render(request, 'programs/program_form.html', {
        'form': form,
        'title': 'Create Program',
    })

@login_required
def program_update(request, pk):
    program = get_object_or_404(HealthProgram, pk=pk)
    
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, f'Program {program.name} updated successfully.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = ProgramForm(instance=program)
    
    return render(request, 'programs/program_form.html', {
        'form': form,
        'program': program,
        'title': 'Update Program',
    })
