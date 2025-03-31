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

# Database configuration (use SQLite for simplicity on Render)
# You can switch to PostgreSQL later if needed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# For Render.com deployment
