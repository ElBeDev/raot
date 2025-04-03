#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "raotproject.production_settings")
django.setup()

# Import Django models and run migrations
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    print("Starting migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("Migrations complete!")
    
    # Check if superuser exists, create if not
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'changeme123')
        print("Superuser created with username 'admin' and password 'changeme123'")
        print("IMPORTANT: Please login and change this password immediately!")

if __name__ == "__main__":
    main()