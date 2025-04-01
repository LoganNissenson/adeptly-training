"""
Production settings for Adeptly project
"""

import os
from .settings import *  # Import base settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Temporarily enable debug for troubleshooting

# Allow the Render.com domain and your custom domain if you have one
ALLOWED_HOSTS = ['*']  # This will allow all hosts temporarily for debugging

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
SECURE_SSL_REDIRECT = False  # Temporarily disable for troubleshooting
SESSION_COOKIE_SECURE = False  # Temporarily disable for troubleshooting
CSRF_COOKIE_SECURE = False  # Temporarily disable for troubleshooting
SECURE_BROWSER_XSS_FILTER = True

# For Render.com deployment

# Configure connection pooling for PostgreSQL
DATABASE_OPTIONS = {
    'connect_timeout': 60,
    'options': '-c statement_timeout=30000'
}

# Make sure migration files use the right column types for PostgreSQL
DATABASE_ENGINE = 'django.db.backends.postgresql'

# Auto-run migrations on startup (for Render.com deployment)
import sys
from django.core.management import call_command

# Only run migrations when not in shell or testing mode
if 'shell' not in sys.argv and 'test' not in sys.argv and 'makemigrations' not in sys.argv:
    try:
        print("Auto-running migrations on startup...")
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connections, DEFAULT_DB_ALIAS
        
        connection = connections[DEFAULT_DB_ALIAS]
        connection.prepare_database()
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        
        # Only run migrations if there are unapplied ones
        if executor.migration_plan(executor.loader.graph.leaf_nodes()):
            call_command('migrate', no_input=True)
            print("Database migrations applied successfully.")
            
            # Now run the setup command to initialize data
            try:
                print("Running Adeptly setup...")
                call_command('setup_adeptly')
                print("Adeptly setup completed successfully.")
            except Exception as e:
                print(f"Error running Adeptly setup: {e}")
    except Exception as e:
        print(f"Error running migrations: {e}")
