#!/bin/bash
# Render Build Script

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations - commented out since not currently needed
# python manage.py migrate

# Initialize application data - commented out since not currently needed
# python manage.py setup_adeptly

# Collect static files
python manage.py collectstatic --no-input

echo "Build script completed successfully!"
