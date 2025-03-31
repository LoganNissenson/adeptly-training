#!/bin/bash

# Create necessary directories
mkdir -p staticfiles
mkdir -p media

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Copy static files directly (bypass Django's collectstatic)
python direct_static.py

# Try Django's collectstatic as well (but don't stop if it fails)
python manage.py collectstatic --no-input || echo "Collectstatic command failed, but we already copied the files directly."
