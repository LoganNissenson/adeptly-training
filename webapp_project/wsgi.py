"""
WSGI config for webapp_project project.
"""

import os
import pathlib
from dotenv import load_dotenv

ENV_PATH = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(ENV_PATH)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings')

application = get_wsgi_application()
