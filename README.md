# Adeptly Training Platform

A training platform for MEP (mechanical, electrical, and plumbing) engineering professionals.

## Deployment Information

### Render.com Free Tier Limitations

When deploying on Render.com's free tier, please be aware of the following limitations:

1. **Database Persistence**: The SQLite database will be reset on each new deployment or when the service restarts. This means any user data, training sessions, or custom problems will be lost.

2. **Initial Data**: The application automatically initializes with basic topics, ranks, and sample engineering problems on each deployment.

3. **Usage Recommendations**:
   - Use the free deployment mainly for demonstration purposes
   - For actual usage, consider upgrading to Render's Starter plan ($7/month) which includes persistent disk storage
   - Alternatively, configure the application to use an external database service

## Local Development

For local development, follow these steps:

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Initialize basic data: `python manage.py initialize_adeptly`
7. Load sample problems: `python manage.py import_engineering_problems`
8. Start the development server: `python manage.py runserver`

## Features

- Customizable training sessions based on topics and difficulty levels
- Experience points and progression system
- Problem management and creation
- Performance tracking and analytics
- Leaderboards

## Project Structure

The project follows a standard Django application structure. The main components are:

- `adeptly/`: Main application package
- `webapp_project/`: Project settings module
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `media/`: User-uploaded files
