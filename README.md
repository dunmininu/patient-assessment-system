# Kochanet Patient Assessment System

## Overview

The Kochanet Patient Assessment System is a backend application designed to manage patient assessments by clinicians. Built using Django and Django REST Framework (DRF), it leverages PostgreSQL for the database and handles user authentication, including email invitations for clinician registration.

The system allows admins to invite clinicians to manage patient assessments, and it includes multi-tenancy support to isolate data for different tenants (clinicians). JWT-based authentication is implemented for secure login.

## Project Structure:

- **Backend**: Django
- **Database**: PostgreSQL
- **API**: Django REST Framework (DRF)
- **Environment Handling**: `django-decouple`
- **Email**: Using Django's `send_mail` (console backend for development)

## Key Features

1. **User Registration & Authentication**:

   - Admins can invite clinicians via email.
   - Clinicians receive an invitation and can register with an inactive account until they accept the invitation.
   - JWT token-based authentication for login (using `rest_framework_simplejwt`).

2. **User Roles**:

   - **Admin**: Can invite clinicians and manage system-wide configurations.
   - **Clinician**: Receives an invitation, manages assessments, and handles patient-related operations.

3. **Email Invitation**:

   - Admins can invite clinicians by sending an email with a custom invite link.
   - Emails are printed to the console in development mode.

4. **Assessment System**:

   - Clinicians can create and manage assessments for patients.
   - Final scores for assessments are calculated based on the answers provided by clinicians.
   - Each assessment and answer is tied to a specific clinician, ensuring multi-tenancy support.

5. **Multi-Tenancy**:

   - Each clinician's data is isolated from other tenants.
   - All patient, assessment, and related data is scoped to the tenant (clinician).

6. **Database Configuration**:
   - PostgreSQL is used for reliable and scalable database management.
   - Environment variables are managed using `django-decouple` for better security and separation of configurations.

## Installation

### Clone the Repository:

```bash
git clone https://github.com/dunmininu/patient-assessment-system.git
cd patient-assessment-system
```

### Install Dependencies:

Ensure you have `pipenv` installed to manage the Python environment and dependencies:

```bash
pipenv install --dev
```

### Set Up Environment Variables:

Create a `.env` file in the root of the project with the following variables:

```bash
DEBUG=True
SECRET_KEY=test
DATABASE_NAME=test
DATABASE_USER=test
DATABASE_PASSWORD=test
DATABASE_HOST=test
DATABASE_PORT=5432
ENVIRONMENT=local
FRONTEND_URL=test
EMAIL_HOST_USER=test
EMAIL_HOST_PASSWORD=test
DEFAULT_FROM_EMAIL=test
```

### Set Up the Database:

Ensure PostgreSQL is installed and running. Then, run the following commands to set up the database:

```bash
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
```

### Run the Development Server:

```bash
pipenv run python manage.py runserver
```

### View Emails in the Console:

For development purposes, invitation emails will be printed to the console.

## API Endpoints

### User Registration & Login:

- **POST** `/api/login/`: Login and retrieve a JWT token.

### Invite Clinician (Admin Only):

- **POST** `/api/register/invite/`: Invite a clinician by sending an email.

### Assessments:

- **POST** `/api/assessments/`: Create a new assessment.
- **GET** `/api/assessments/`: Retrieve a list of assessments.
- **GET** `/api/assessments/{id}/`: Retrieve details of a specific assessment.
- **PATCH** `/api/assessments/{id}/`: Update an existing assessment.
- **DELETE** `/api/assessments/{id}/`: Delete an assessment.

## Progress So Far

- PostgreSQL database has been configured with `django-decouple` for environment variable management.
- Custom user model implemented with role-based fields (Admin, Clinician).
- JWT authentication integrated using `rest_framework_simplejwt`.
- Admins can invite clinicians to the platform via email.
- Console email backend is set up to display invitation emails in the development environment.
- Assessment models created, including multi-tenancy support for tenant-based isolation of data.
- Implement clinician registration and account activation via the invite link.
- Add CRUD operations for managing patients.
- Finalize assessment creation and management features (e.g., score calculation, filters, and pagination).
- Extend the email system to support production-ready email delivery (e.g., using SMTP or a third-party email service).
- Implement more robust multi-tenancy features to further isolate data for different users and tenants.

## Next Steps

- Submit and make a video

---

### Additional Notes

- **Multi-Tenancy**: Ensured that tenant-scoped data is handled properly by using the tenant field in models like `Assessment`, `Patient`, `Question`, and `Answer`. This isolates data based on the clinician.

### Explanation of the AWS Deployment Process

Deploying a Django application on AWS can involve several steps, typically utilizing services such as Amazon EC2, RDS, and S3. I would use EC2 in this case

#### 1. **Set Up AWS Account**

- Create an AWS account if you don’t already have one.
- You would need a card if you're setting up a new account, aws will charge you a dollar and refund it later. it's just to check that your card is active
- Log in to the AWS Management Console.

#### 2. **Launch an EC2 Instance**

- Go to the **EC2 Dashboard**.
- Click on **Launch Instance** and select an Amazon Machine Image (AMI). For Django, an Ubuntu or Amazon Linux AMI is commonly used. I am going with the Ubuntu instance, this one I am comfortable with. for testing purposes, you can choose the free tier volume type
- Choose an instance type based on your application’s requirements (e.g., t2.micro for testing, also free).
- for the key pair, you can choose an existing one or create one on the fly, but make sure to download it after creation
- Configure instance details, including network settings and IAM roles if needed.
- Add storage as per your application needs.
- Configure security group settings to allow HTTP (port 80), HTTPS (port 443), and SSH (port 22) access.
- Launch the instance and download the key pair (.pem file) for SSH access.

#### 3. **Connect to the EC2 Instance**

- Use SSH to connect to your EC2 instance. Use the following command:

```bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-dns
```

#### 4. **Install Required Software**

- Update the package manager:

```bash
sudo apt update
sudo apt upgrade
```

- Install necessary packages (Python, pip, virtualenv, and a web server):

```bash
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

- Install `git` to clone your repository:

```bash
sudo apt install git
```

#### 5. **Clone Your Django Application**

- Clone your application repository from GitHub or any other version control service:

```bash
git clone https://github.com/dunmininu/patient-assessment-system.git
cd patient-assessment-system
```

#### 6. **Set Up a Virtual Environment**

- Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install your project dependencies:

```bash
pip install -r requirements.txt
```

#### 7. **Configure the Database**

- Set up a PostgreSQL database using RDS (or use a local database on the EC2 instance).
  - If using RDS:
    - Create a new RDS instance in the AWS Management Console.
    - Note the endpoint, database name, username, and password.
      (note: we shall not use this for cost efficiency on testing)
  - If using a local PostgreSQL database, set it up accordingly.
- Update your Django `.env` with the database credentials.

#### 8. **Migrate Database**

- Run migrations to set up the database schema:

```bash
python manage.py migrate
```

#### 9. **Collect Static Files**

- Collect static files to serve them using Nginx:

```bash
python manage.py collectstatic
```

#### 10. **Configure Gunicorn**

- Install Gunicorn:

```bash
pip install gunicorn
```

- Run your application using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 patient_assessment.wsgi:application
```

#### 11. **Configure Nginx**

- Create a new Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/patient_assessment
```

- Add the following configuration:

```nginx
server {
    listen 80;
    server_name your_domain_or_public_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/your/static/files; <!-- this is the static files directory that was created after running collectstatic above -->
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/your/your_project.sock;
    }
}
```

- Enable the configuration by creating a symbolic link:

```bash
sudo ln -s /etc/nginx/sites-available/patient_assessment /etc/nginx/sites-enabled
```

- Test the Nginx configuration:

```bash
sudo nginx -t
```

- Restart Nginx:

```bash
sudo systemctl restart nginx
```

#### 12. **Domain Configuration (Optional)**

- If you have a domain name, configure it to point to your EC2 instance's public IP address. (just a thought, I can't elaborate on this)

#### 13. **Security Configuration**

- Set up SSL certificates using Let's Encrypt for secure HTTPS connections.
- Adjust security group settings in AWS to limit access to your instance.
