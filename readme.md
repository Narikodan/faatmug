# Vendor Management System

This project is a Django-based Vendor Management System with a RESTful API. It includes views for managing vendors, purchase orders, and related data. This README provides setup instructions, test suite execution, and other relevant information.

## Requirements

- Python 3.8 or later
- Django 5.0.4 or later
- PostgreSQL or your preferred database engine
- Virtualenv or a similar virtual environment manager

## Setup

To set up this project on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2.Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
Ensure that PostgreSQL is installed and running. Update the DATABASES setting in settings.py to match your PostgreSQL setup. The default configuration is as follows:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vendormanagement',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',}}
            
```
Adjust the NAME, USER, PASSWORD, HOST, and PORT as needed.

### 5. Apply Migrations and Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser  # Follow the prompts to create a superuser
```
### 6. Run the Server
```bash 
python manage.py runserver
```
The server will start on http://127.0.0.1:8000/. You can access the Django admin site at /admin with the superuser credentials created earlier.

### Authentication
The project uses TokenAuthentication and SessionAuthentication for REST API endpoints. Ensure you have valid tokens or a valid session for authentication.

### Running Tests
To run the test suite, use the following command:

```bash
python manage.py test
```
This will run all tests defined in the tests.py file. Ensure your test cases are comprehensive and cover all necessary scenarios.

### Project Structure
    - vendor_management_system/: Main project directory
    - vendor_management/: Django app containing views, models, serializers, etc.
    - tests.py: Test cases for the Django app
    - requirements.txt: Project dependencies
    - manage.py: Django's command-line utility
    - settings.py: Django project settings

