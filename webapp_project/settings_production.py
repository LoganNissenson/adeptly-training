"""
Production settings for Adeptly project
"""

import os
from .settings import *  # Import base settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow the Render.com domain and your custom domain if you have one
ALLOWED_HOSTS = ['adeptly.onrender.com', '.yourdomain.com']  # Update with your actual domain

# Configure static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Add WhiteNoise middleware for static files
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database configuration using PostgreSQL on Render
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        # This will use the DATABASE_URL environment variable from Render
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# For Render.com deployment

# Configure connection pooling for PostgreSQL
DATABASE_OPTIONS = {
    'connect_timeout': 60,
    'options': '-c statement_timeout=30000'
}

# Make sure migration files use the right column types for PostgreSQL
DATABASE_ENGINE = 'django.db.backends.postgresql'
