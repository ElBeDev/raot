"""
PRODUCTION SETTINGS TEMPLATE
Copy this file to settings_local.py on your production server
"""

from pathlib import Path
import os
from .settings import *

# Use SQLite for local development (simpler than remote PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug settings for development
DEBUG = True
ALLOWED_HOSTS = ['*']

# Override STATIC_URL and STATIC_ROOT for local development
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')