# Health Information System

A comprehensive web application for managing clients and health programs, built with Django and Bootstrap.


## Overview

This Health Information System allows healthcare providers to manage client information, health programs, and program enrollments. The system provides a user-friendly interface for tracking client participation in various health programs such as TB, Malaria, HIV, and more.

## Features

- **User Authentication**
  - Secure email-based login and registration
  - Custom user model with user roles
  - Password reset functionality

- **Client Management**
  - Register new clients with personal and contact information
  - Search clients by name, email, or phone number
  - View detailed client profiles
  - Update client information

- **Health Programs**
  - Create and manage health programs
  - Track program status (active, planned, completed)
  - Monitor program capacity and enrollment
  - Filter programs by status

- **Enrollment Management**
  - Enroll clients in multiple health programs
  - Track enrollment status and history
  - View enrolled clients by program

- **Dashboard**
  - Overview of system statistics
  - Quick access to recent clients and active programs
  - Visual indicators of system activity

## Technology Stack

- **Backend**: Django
- **Frontend**: Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Forms**: Django Forms with Crispy Forms
- **Authentication**: Django's built-in authentication system
- **Testing**: Django Test Framework with pytest and unittest na locust

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/https://github.com/solo925/CEMA-HEALTH.git
   cd CEMA-HEALTH
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv Venv
   source Venv/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://localhost:8000/

## Project Structure

```
health_system/
├── accounts/               # User authentication app
├── clients/                # Client management app
├── programs/               # Health programs app
├── health_system/          # Project settings folder
├── static/                 # Static files
├── templates/              # Global templates
├── media/                  # User uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Project dependencies
└── db.sqlite3              # Development database
```

## Testing

The project includes comprehensive tests for models, forms, views, and URLs. To run the tests:

```bash
python manage.py test
```

For more detailed test output:

```bash
python -m pytest
```

## API Documentation

The system exposes client profiles via a RESTful API:

- **GET /api/clients/** - List all clients
- **GET /api/clients/{id}/** - Retrieve a specific client profile
- **GET /api/programs/** - List all health programs
- **GET /api/programs/{id}/** - Retrieve a specific program

Authentication is required to access the API endpoints.

## Design Decisions

1. **Django Templates over React/Angular**
   - Single technology stack for easier maintenance
   - Simplified development process
   - Built-in form validation and CSRF protection

2. **Bootstrap for Responsive Design**
   - Mobile-friendly interface
   - Consistent UI components
   - Rapid development of responsive layouts

3. **Custom User Model**
   - Email-based authentication instead of username
   - Future-proofing for potential authentication changes

4. **UUID Primary Keys**
   - Enhanced security for public-facing IDs
   - Protection against enumeration attacks
   - Guaranteed uniqueness across database tables



## Chaos Testing, Load Testing, and Monitoring

## DevOps for Development

### Load Testing

Load testing helps ensure the application can handle expected traffic and identifies performance bottlenecks before they affect users.

#### Installation:

```bash
pip install locust
```

Run the load test:

```bash
locust -f load_test/locustfile.py --host=http://localhost:8000
```

Access the Locust web interface at http://localhost:8089 to start the test.

### Chaos Testing

Chaos testing helps ensure the system can recover from unexpected failures.

#### Installation:

```bash
pip install chaosmonkey
```
Run with chaos testing enabled:

```bash
ENABLE_CHAOS=True python manage.py runserver
```

### Monitoring
- Prometheus metrics for performance tracking
- Grafana dashboards for visualization
- Sentry integration for error tracking
