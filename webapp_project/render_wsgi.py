"""
Special WSGI module for Render.com
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Django settings to production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings_production')

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure static and media directories exist
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Create directories if they don't exist
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Import the standard WSGI application
from webapp_project.wsgi import application
