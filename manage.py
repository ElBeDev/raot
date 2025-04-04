#!/usr/bin/env python
import os
import sys

def main():
    # Try to use settings_local if it exists
    try:
        from raotproject import settings_local
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raotproject.settings_local')
    except ImportError:
        # Check that it's using the main settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raotproject.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
