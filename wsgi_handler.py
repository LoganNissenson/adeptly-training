"""
WSGI handler for Render.com deployment
"""

import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.render')

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
