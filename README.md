# Interns Rizz

Interns Rizz is a Django-based job and internship discovery platform designed for students and freshers.

The idea is to make finding internships and jobs easier through a swipe-based interface. Users can create their profile, upload their resume, discover jobs based on their profile, and apply for opportunities.

## Features

* User registration and login
* User profile creation
* Resume upload
* Job and internship listings
* Job filtering
* Swipe-based job discovery
* Job match percentage
* Save and reject jobs
* Resume modification for specific jobs
* Personalized job recommendations

## Tech Stack

* Python
* Django
* HTML
* CSS
* JavaScript
* SQLite for development
* PostgreSQL for production

## Project Structure

```text
internsrizz/
│
├── manage.py
├── internsrizz/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── interns_app/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── media/
│   └── resumes/
│
├── static/
│
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/internsrizz.git
```

Go to the project directory:

```bash
cd internsrizz
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Adding Jobs

Jobs can currently be added through the Django Admin panel.

Open:

```text
http://127.0.0.1:8000/admin/
```

Log in using the superuser account and add jobs from the Jobs section.

## Resume Uploads

User resumes are stored using Django's `FileField`.

Uploaded resumes should not be committed to GitHub.

Add the following to `.gitignore`:

```gitignore
media/
venv/
__pycache__/
*.pyc
.env
db.sqlite3
```

## Current Status

The following features are currently implemented:

* Authentication
* Signup and login
* Profile setup
* Resume upload
* Job model
* Job management through Django Admin
* Job feed
* Dynamic job data

Features planned for future development:

* Swipe functionality
* Job matching algorithm
* Match percentage calculation
* Save and reject functionality
* Application tracking
* Resume modification
* Skill gap detection
* Personalized job recommendations
* Company dashboard

## Purpose

Interns Rizz is being developed as a project to explore Django, authentication, database management, file uploads, job matching, and full-stack web development.

## Author

Built as a BCA student project using Python and Django.
