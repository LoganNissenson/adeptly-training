"""
Script to export data from SQLite database to a JSON file.
Run this first before switching to PostgreSQL.
"""

import os
import sys
import django
import json
from django.core import serializers
from django.core.management import call_command

def main():
    print("Starting data export from SQLite database...")
    
    # Force Django to use SQLite by setting USE_SQLITE environment variable
    os.environ['USE_SQLITE'] = 'true'
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings')
    
    # Initialize Django
    django.setup()
    
    # Use a more controlled approach to handle encoding issues
    try:
        # First, get the data using dumpdata command, but don't write to a file yet
        print("Fetching data from SQLite database...")
        data = serializers.serialize(
            "json", 
            get_all_objects(),
            indent=4,
            ensure_ascii=True  # This handles encoding issues
        )
        
        # Write the data to a file with explicit encoding
        with open('data_dump.json', 'w', encoding='utf-8') as f:
            f.write(data)
        
        print("\n✅ Data export completed successfully!")
        print("Data has been saved to data_dump.json")
        print("\nTo import this data to PostgreSQL:")
        print("1. Edit your .env file with the correct PostgreSQL credentials")
        print("2. Run: python import_postgres_data.py")
    
    except Exception as e:
        print(f"\n❌ Error during data export: {e}")
        print("Try running the export with default Django commands:")
        print("python manage.py dumpdata --exclude=contenttypes --exclude=auth.permission > data_dump.json")

# Helper function to get all objects except contenttypes and permissions
def get_all_objects():
    from django.apps import apps
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    
    all_objects = []
    
    for model in apps.get_models():
        # Skip ContentType and Permission models
        if model == ContentType or model == Permission:
            continue
        
        # Get all objects for this model
        try:
            objects = model.objects.all()
            all_objects.extend(objects)
        except Exception as e:
            print(f"Warning: Could not fetch objects for {model.__name__}: {e}")
    
    return all_objects

if __name__ == "__main__":
    main()
