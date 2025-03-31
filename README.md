# Adeptly Training

A Django web application for MEP (mechanical, electrical, and plumbing) engineering firms to monitor and grow the core knowledge base of their employees.

## Overview

Adeptly is a platform that allows MEP engineering professionals to:

- Practice with customized training sessions based on topics and difficulty
- Track progress and experience earned across different engineering topics
- Prepare for professional engineering exams with targeted practice problems

The platform also enables managers to:
- Objectively assess employee competency across topics
- Identify areas where employees may need additional training
- Provide specific practice problems for struggling topics

## Setup Instructions

1. Clone the repository to your local machine.
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py makemigrations adeptly
   python manage.py migrate
   ```
6. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```
8. Access the application in your browser at http://127.0.0.1:8000/

## Initial Setup

After installation, you'll need to:

1. Create topics in the admin interface (e.g., HVAC Design, Electrical Code, Plumbing Systems)
2. Create ranks (e.g., Beginner, Intermediate, Advanced, Expert)
3. Add training problems with answers, topics, difficulty levels, and time estimates

## Features

- User authentication and profiles
- Training session setup with customizable parameters
- Multiple-choice problem interface with interactive elements
- Experience tracking and statistics
- Problem management interface

## Project Structure

- `adeptly/`: Main application code
  - `models.py`: Database models (User, Topic, Problem, etc.)
  - `views.py`: View functions and classes
  - `forms.py`: Form classes
  - `urls.py`: URL patterns
- `templates/`: HTML templates
  - `base.html`: Base template with common elements
  - `adeptly/`: Application-specific templates
- `static/`: Static files (CSS, JavaScript)
- `media/`: User-uploaded files (problem diagrams)

## Color Palette

Based on HVAC equipment colors:
- Light Gray: #DBE0DE
- Dark Blue: #172532
- Blue: #88B6CD
- Medium Gray: #7E8B90
- Light Blue-Gray: #B7C3BF
#test comment 
