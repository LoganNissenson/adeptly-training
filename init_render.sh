#!/bin/bash

# Create necessary directories for static files and media
mkdir -p staticfiles
mkdir -p media

# Install dependencies
pip install -r requirements.txt

# Run migrations with output (helpful for debugging)
python manage.py migrate --noinput

# Initialize basic data
python manage.py initialize_adeptly

# Import engineering problems
python manage.py import_engineering_problems

# Copy static files directly (bypass Django's collectstatic)
python direct_static.py

# Try Django's collectstatic as well (but don't stop if it fails)
python manage.py collectstatic --no-input || echo "Collectstatic command failed, but we already copied the files directly."
