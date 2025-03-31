# Adeply Project Summary

## Project Overview

Adeply (Adeptly Training) is a Django web application designed for MEP (mechanical, electrical, and plumbing) engineering firms to train and track the progress of their employees' technical knowledge. The platform allows engineering professionals to practice with customized training sessions based on specific topics and difficulty levels, while enabling managers to objectively assess employee competency and identify areas requiring additional training.

The core purpose of Adeply is to:
- Help engineering professionals prepare for professional exams
- Provide targeted practice in specific engineering domains
- Track progress and experience points earned across different engineering topics
- Allow organizations to objectively measure employee knowledge growth

## Technical Architecture

Adeply is built with the following technologies:

- **Frontend**:
  - HTML/CSS/JavaScript
  - Bootstrap or custom CSS framework using a color palette based on HVAC equipment colors
  - Django Templates for rendering views

- **Backend**:
  - Django (Python web framework)
  - SQLite database (default, can be migrated to PostgreSQL for production)
  - Django ORM for database interactions

- **Deployment/Environment**:
  - Python virtual environment
  - Local development server (Django's built-in server)
  - Can be deployed to standard web hosting platforms with Python support

- **Authentication**:
  - Django's built-in authentication system
  - User roles (regular users, administrators)

## Key Features and Components

1. **User Authentication System**
   - Login/logout functionality
   - User profiles
   - Role-based access control (regular users vs. administrators)

2. **Training System**
   - Customizable training sessions
   - Problem selection based on topic, difficulty, and available time
   - Multiple-choice problem interface with answer validation
   - Problem diagrams for visual reference
   - Timed training sessions

3. **Experience and Progression System**
   - Experience points awarded based on problem difficulty
   - Topic-specific experience tracking
   - Rank progression (Beginner, Intermediate, Advanced, Expert)
   - Performance statistics and metrics

4. **Administrative Features**
   - Problem management (create, edit, delete)
   - User statistics and progress monitoring
   - Topic and rank management

5. **Reporting and Analytics**
   - Personal progress dashboards
   - Leaderboards (overall and topic-specific)
   - Training session results and analytics

## Project Structure

The project follows a standard Django application structure:

```
django_webapp/
├── adeptly/                  # Main application package
│   ├── admin.py              # Admin site configuration
│   ├── apps.py               # Application configuration
│   ├── forms.py              # Form definitions
│   ├── management/           # Custom management commands
│   │   └── commands/         # Contains custom commands like initialize_adeptly
│   ├── migrations/           # Database migrations
│   ├── models.py             # Database models
│   ├── problem_diagrams/     # Default problem diagrams
│   ├── templatetags/         # Custom template tags
│   ├── tests.py              # Test suite
│   ├── urls.py               # URL routing
│   └── views.py              # View functions and classes
├── media/                    # User-uploaded files
│   ├── problem_diagrams/     # Uploaded problem diagrams
│   └── solution_diagrams/    # Uploaded solution diagrams
├── static/                   # Static files (CSS, JS, images)
├── templates/                # HTML templates
│   └── adeptly/              # Application-specific templates
├── manage.py                 # Django command-line utility
├── requirements.txt          # Python dependencies
└── webapp_project/           # Project settings module
```

## Data Models

The application uses the following key data models:

1. **User** (extends Django's built-in User model)
   - Authentication credentials
   - Basic profile information

2. **Topic**
   - Represents a specific engineering domain (e.g., HVAC Design, Electrical Systems)
   - Name field

3. **Rank**
   - Represents skill/knowledge levels (e.g., Beginner, Intermediate, Advanced, Expert)
   - Name field

4. **Problem**
   - Training problems with multiple-choice answers
   - Fields: name, prompt, choices A-D, correct answer, difficulty (1-5)
   - Many-to-many relationship with Topics
   - Optional diagram attachments
   - Estimated time to complete

5. **UserTopicStats**
   - Links users to topics with experience points and rank
   - Fields: user, topic, experience, rank

6. **TrainingSession**
   - Represents a single training activity
   - Fields: user, problems, topics covered, completion status, statistics
   - Timestamps for created_at and completed_at

7. **TopicExperienceEarned**
   - Records experience points earned for specific topics
   - Fields: user, topic, experience_earned, training_session, problem

## Workflow Examples

### Regular User Workflow:
1. User logs in to the system
2. Views personalized dashboard showing progress stats
3. Initiates new training session
4. Selects topics, difficulty levels, and available time
5. Completes training problems, receiving immediate feedback
6. Reviews session results and experience earned
7. Tracks progress over time via dashboard and leaderboards

### Administrator Workflow:
1. Admin logs in with administrator credentials
2. Manages problem database (adds, edits, or removes problems)
3. Reviews user statistics and performance metrics
4. Configures topics and ranks as needed
5. Monitors overall system usage and engagement

This summary provides an overview of the Adeply project, its architecture, features, and structure to help Claude effectively assist with development tasks.
