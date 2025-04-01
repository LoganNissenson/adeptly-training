"""
Script to run migrations on a remote PostgreSQL database.
Use this to migrate your Render.com database without shell access.
"""

import os
import sys
import django
from django.core.management import call_command
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    print("Loading environment variables from .env file...")
    load_dotenv()
    
    print("Starting remote database migration...")
    
    # Check if DATABASE_URL is set and uncommented in .env
    db_url = os.environ.get('DATABASE_URL', '')
    print(f"DATABASE_URL found: {'Yes' if db_url else 'No'}")
    if db_url:
        print(f"URL contains 'render.com': {'Yes' if 'render.com' in db_url else 'No'}")
    
    if not db_url or db_url.startswith('#'):
        print("❌ Error: DATABASE_URL is not set or is commented out in your .env file!")
        print("Please edit your .env file and add your Render.com external database URL.")
        sys.exit(1)
    
    # Check if the URL contains render.com to verify it's a remote database
    if 'render.com' not in db_url:
        print("⚠️  Warning: Your DATABASE_URL doesn't contain 'render.com'.")
        print(f"DATABASE_URL: {db_url}")
        response = input("Are you sure this is your Render.com database? (y/n): ")
        if response.lower() != 'y':
            print("Aborting migration.")
            sys.exit(1)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings_production')
    
    # Initialize Django
    django.setup()
    
    # Check connection
    from django.db import connection
    try:
        connection.ensure_connection()
        print(f"✅ Successfully connected to remote database: {connection.vendor}")
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        sys.exit(1)
    
    # Run migrations
    print("\nRunning migrations...")
    call_command('migrate')
    
    # Initialize app data
    print("\nInitializing application data...")
    try:
        # Check if Topic model has any data
        from adeptly.models import Topic
        if Topic.objects.count() == 0:
            print("Running initialize_adeptly command...")
            call_command('initialize_adeptly')
        else:
            print("Topics already exist, skipping initialize_adeptly.")
            
        # Check if Problem model has any data
        from adeptly.models import Problem
        if Problem.objects.count() == 0:
            print("Running import_engineering_problems command...")
            call_command('import_engineering_problems')
        else:
            print("Problems already exist, skipping import_engineering_problems.")
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
    
    print("\n✅ Remote database setup completed!")
    print("Your Render.com PostgreSQL database should now be ready to use.")

if __name__ == "__main__":
    main()
