"""
Script to import data from a JSON file into a PostgreSQL database.
Run this after export_sqlite_data.py and setting up PostgreSQL.
"""

import os
import sys
import django
import json
from django.core.management import call_command
from django.db import connection
from django.core import serializers

def main():
    print("Starting data import to PostgreSQL database...")
    
    # Ensure we're using PostgreSQL (remove USE_SQLITE if it exists)
    if 'USE_SQLITE' in os.environ:
        del os.environ['USE_SQLITE']
    
    # Check if data_dump.json exists
    if not os.path.exists('data_dump.json'):
        print("❌ Error: data_dump.json not found!")
        print("Please run export_sqlite_data.py first.")
        sys.exit(1)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings')
    
    # Initialize Django
    django.setup()
    
    # Check if we're connected to PostgreSQL
    db_engine = connection.vendor
    if db_engine != 'postgresql':
        print(f"❌ Error: Not connected to PostgreSQL! Current database: {db_engine}")
        print("Check your .env file and make sure DATABASE_URL is set correctly.")
        sys.exit(1)
    
    print("Connected to PostgreSQL database successfully!")
    
    # Run migrations first
    print("\nRunning migrations...")
    call_command('migrate')
    
    # Clear ContentType table to avoid conflicts
    print("\nClearing ContentType table...")
    try:
        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.all().delete()
        print("ContentType table cleared successfully!")
    except Exception as e:
        print(f"Warning: Could not clear ContentType table: {e}")
    
    # Import data with better error handling
    print("\nImporting data from data_dump.json...")
    try:
        # Read the data file with explicit encoding
        with open('data_dump.json', 'r', encoding='utf-8') as f:
            data = f.read()
        
        # Process the data
        for obj in serializers.deserialize('json', data):
            try:
                obj.save()
            except Exception as e:
                print(f"Warning: Could not save object {obj.object.__class__.__name__} - {e}")
        
        print("\n✅ Data import completed successfully!")
        print("Your PostgreSQL database now contains all the data from SQLite.")
        print("\nYou can now run the Django server with: python manage.py runserver")
    
    except Exception as e:
        print(f"\n❌ Error during data import: {e}")
        print("\nAlternative method:")
        print("1. Try using loaddata directly:")
        print("   python manage.py loaddata data_dump.json")
        print("2. If that fails, you may need to manually recreate your data in PostgreSQL")

if __name__ == "__main__":
    main()
