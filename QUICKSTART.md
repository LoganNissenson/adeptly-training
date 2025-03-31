# Adeptly Training - Quick Start Guide

This quick start guide will help you get the Adeptly Training application up and running quickly.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional)

## Installation Steps

1. **Activate your virtual environment**

   ```bash
   # If you haven't created a virtual environment yet
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py makemigrations adeptly
   python manage.py migrate
   ```

4. **Initialize the application with default data**

   ```bash
   python manage.py initialize_adeptly
   ```

5. **Create an administrator account**

   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create a username, email, and password.

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**

   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Initial Configuration

After installation, follow these steps to configure your Adeptly instance:

1. **Log in to the admin interface** (http://127.0.0.1:8000/admin/) using the superuser credentials you created.

2. **Add or modify Topics** 
   - Navigate to Topics in the admin panel
   - The initialization script created some default topics, but you can add more specific to your organization's needs

3. **Add Problems**
   - Navigate to Problems in the admin panel
   - Create problems with:
     - A clear prompt
     - Four answer choices (A, B, C, D)
     - Specify the correct answer
     - Set difficulty (1-5)
     - Assign relevant topics
     - Upload diagram images if needed

4. **Create regular user accounts**
   - Create accounts for employees who will use the system
   - These users will have access to training but not admin features

## Basic Usage

### For Employees (Regular Users)

1. **Log in** to the application
2. **Dashboard** - View your statistics and training progress
3. **Start Training** - Set up a custom training session:
   - Select topics to practice
   - Choose difficulty levels
   - Set available training time
4. **Complete training sessions** - Answer questions and earn experience points
5. **Review results** - See performance statistics and areas for improvement

### For Administrators

1. **Manage Problems** - Add, edit, and delete training problems
2. **View User Statistics** - Monitor employee performance and progress
3. **Add Topics** - Expand the training material coverage

## Troubleshooting

- If you encounter database issues, try:
  ```bash
  python manage.py migrate --run-syncdb
  ```

- If static files aren't loading correctly:
  ```bash
  python manage.py collectstatic
  ```

- For permission issues with media uploads, ensure your media directory is writable by the web server.

## Next Steps

After initial setup, consider:

1. Adding more problems to build a comprehensive question bank
2. Customizing the topics to match your organization's specific needs
3. Setting up regular training sessions for your team
4. Reviewing user statistics to identify knowledge gaps
