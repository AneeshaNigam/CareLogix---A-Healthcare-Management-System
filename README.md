# CareLogix - Healthcare Management System

## Project Overview

CareLogix is a Django-based healthcare management system that allows medical professionals to manage patient records, doctor information, and patient-doctor relationships through a secure API.

## Project Structure

```
CareLogix/
├── api/                          # Main application
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Database models
│   ├── serializers.py            # DRF serializers
│   ├── tests.py                  # Test cases
│   ├── urls.py                   # App URL routes
│   └── views.py                  # API views
├── CareLogix/                    # Project settings
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL routes
│   └── wsgi.py                   # WSGI configuration
├── templates/                    # HTML templates
│   └── home.html                 # Homepage template
├── .env                          # Environment variables
├── .gitignore                    # Git ignore rules
├── manage.py                     # Django management script
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/AneeshaNigam/CareLogix---A-Healthcare-Management-System.git CareLogix
   cd CareLogix
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**

   - Create a database named `carelogix_db`
   - Update the `.env` file with your database credentials:
     ```env
     DB_NAME=carelogix_db
     DB_USER=your_username
     DB_PASSWORD=your_password
     DB_HOST=localhost
     DB_PORT=5432
     SECRET_KEY=your-secret-key
     DEBUG=True
     ```

5. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login

### Patient Management

- `POST /api/patients/` - Create patient
- `GET /api/patients/` - List all patients
- `GET /api/patients/<id>/` - Get patient details
- `PUT /api/patients/<id>/update/` - Update patient
- `DELETE /api/patients/<id>/delete/` - Delete patient

### Doctor Management

- `POST /api/doctors/` - Create doctor
- `GET /api/doctors/` - List all doctors
- `GET /api/doctors/<id>/` - Get doctor details
- `PUT /api/doctors/<id>/update/` - Update doctor
- `DELETE /api/doctors/<id>/delete/` - Delete doctor

### Patient-Doctor Mapping

- `POST /api/mappings/` - Assign doctor to patient
- `GET /api/mappings/` - List all mappings
- `GET /api/mappings/<patient_id>/` - Get doctors for a patient
- `DELETE /api/mappings/<id>/delete/` - Remove mapping

## Testing the API

Use tools like **Postman** or **Thunder Client** to test the endpoints:

1. Start with user registration or login to get JWT tokens
2. Use the access token in the Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```
3. Test the various endpoints with sample data

## Key Features

- JWT Authentication for secure access
- RESTful API design
- PostgreSQL database for reliable data storage
- Patient and doctor management
- Relationship mapping between patients and doctors
- Error handling and validation

## Technologies Used

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Python-decouple for environment variables
