Kochanet Patient Assessment System

Overview

    This is a backend application for a patient assessment system where clinicians can manage patient assessments.
    The application is built using Django and Django REST Framework (DRF), with PostgreSQL as the database. Clinicians can be invited by admins to manage assessments, and the system includes user authentication and email invitation features.

Project Structure:

    Backend: Django
    Database: PostgreSQL
    API: Django REST Framework (DRF)
    Environment Handling: django-decouple
    Email: Django's send_mail (console backend for development)

Key Features

    User Registration & Authentication:
    Admins can invite clinicians via email.
    Clinicians are registered with an inactive account until they accept the invitation.
    JWT token-based authentication for login (using rest_framework_simplejwt).

User Roles:

    Admin: Can invite clinicians.
    Clinician: Receives invitation and manages assessments.

Email Invitation:

    Admins invite clinicians by sending an email with a custom invite link.
    Emails are currently printed to the console for development purposes.

Database Configuration:

    PostgreSQL is used for database management.
    Environment variables are managed using django-decouple.

Installation
Clone the Repository:

    ```git clone https://github.com/your_username/kochanet-patient-assessment.git```
    ```cd kochanet-patient-assessment```

Install Dependencies: Ensure you have pipenv installed:

    ```pipenv install --dev```

Set Up Environment Variables: Create a .env file in the root of the project:

    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://username:password@localhost:5432/yourdbname
    FRONTEND_URL=https://your-frontend-url.com

Set Up the Database: Make sure PostgreSQL is installed and running. Run the following commands to set up your database:

    ```pipenv run python manage.py migrate```
    ```pipenv run python manage.py createsuperuser```

Run the Development Server:

    pipenv run python manage.py runserver

View Emails in Console: For now, invitation emails are printed in the console for development purposes.

API Endpoints

User Registration & Login:

    POST /api/login/: Login and retrieve JWT token.
    Invite Clinician (Admin Only):
    POST /api/register/invite/: Invite a clinician by sending an email.

Progress So Far

    Configured PostgreSQL database with django-decouple for environment variable management.
    Implemented custom user model with role field (Admin, Clinician).
    Implemented JWT authentication using rest_framework_simplejwt.
    Admin-only invitation feature added to allow admins to invite clinicians.
    Configured email invitations to print to the console using Django's console email backend for development.

Next Steps

    Implement clinician registration and account activation via the invite link.
    Add patient management (CRUD operations for patients).
    Implement assessment creation and management (including filters, pagination, etc.).
    Implement multi-tenancy to isolate data for different users.

Deployment to AWS

To deploy the application to AWS, follow these steps:

    Set up an EC2 Instance:
    Launch an Ubuntu EC2 instance.
    SSH into the instance and install dependencies such as Python, PostgreSQL, and nginx.

    Install Django & PostgreSQL:
    Set up a virtual environment for the project and install dependencies.
    Set Up Gunicorn:
    Install Gunicorn to serve the Django application.
    Configure systemd to run Gunicorn as a service.
    Configure Nginx:
    Install and configure nginx as a reverse proxy to pass requests to Gunicorn.
    Database Configuration:

    Set up a PostgreSQL instance either locally on the EC2 machine or using Amazon RDS.
    Update environment variables accordingly.

Handle Static Files:

    Use Django's collectstatic to handle static files.
    Configure AWS S3 or other static file storage services if needed.
    Domain & SSL:
    Use AWS Route 53 to manage your domain.
    Set up SSL certificates using Let’s Encrypt and configure them in nginx.

Challenges Faced

    Handling email invitation logic and permissions.
    Ensuring proper permissions between admins and clinicians.
    Additional Features to Be Added
    Fully functional clinician registration using invite links.
    Patient and assessment management with multi-tenancy support.
    Proper production-ready email sending configuration using SMTP.
