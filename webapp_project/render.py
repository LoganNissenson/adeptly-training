"""
Render.com settings for Adeptly project
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-dev-key-do-not-use-in-production')

# Set debug to True temporarily to see detailed error messages
DEBUG = True

# Print settings for debugging
print("BASE_DIR:", BASE_DIR)

# Allow Render.com domains and your custom domain
ALLOWED_HOSTS = ['adeptly-training.onrender.com', 'adeptly.onrender.com', '.render.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adeptly',  # Main application
    'whitenoise.runserver_nostatic',  # WhiteNoise for static files
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cors_middleware.CorsMiddleware',  # Add CORS middleware
]

ROOT_URLCONF = 'webapp_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'adeptly.context_processors.adeptly_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'webapp_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Make sure the static directory exists and print debug info
print("STATIC_ROOT:", STATIC_ROOT)
print("STATICFILES_DIRS:", STATICFILES_DIRS)

import os.path
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
    print(f"Created directory: {STATIC_ROOT}")
else:
    print(f"Directory already exists: {STATIC_ROOT}")
    
# Create a simple static file directly (bypass Django if needed)
empty_css = os.path.join(STATIC_ROOT, 'empty.css')
if not os.path.exists(empty_css):
    with open(empty_css, 'w') as f:
        f.write('/* Empty file */\n')
    print(f"Created file: {empty_css}")

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login redirect
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'

# Security settings
# Temporarily disable these security settings to troubleshoot the 400 error
SECURE_SSL_REDIRECT = False  # Set to True after fixing the 400 error
SESSION_COOKIE_SECURE = False  # Set to True after fixing the 400 error
CSRF_COOKIE_SECURE = False  # Set to True after fixing the 400 error
SECURE_BROWSER_XSS_FILTER = True
