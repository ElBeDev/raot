from pathlib import Path
import os
from .settings import *

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['www.raotsuplementos.com.mx', 'raotsuplementos.com.mx', '69.62.95.109']

# Security settings
SECRET_KEY = 'your-new-secure-production-key'  # Change this!
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raot_db',
        'USER': 'admin',
        'PASSWORD': 'RaotSuper2025',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

# Static and Media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/media'

# CLIP Payment settings
CLIPMX = {
    'API_KEY': 'b8021bcd-4e74-4068-b53b-50c72d4cb80b',
    'SECRET_KEY': '00a1f194-a240-44ad-86e2-ae352679514b',
    'TOKEN': 'Basic YjgwMjFiY2QtNGU3NC00MDY4LWI1M2ItNTBjNzJkNGNiODBiOjAwYTFmMTk0LWEyNDAtNDRhZC04NmUyLWFlMzUyNjc5NTE0Yg==',
    'MODE': 'live',
    'WEBHOOK_SECRET': 'your-webhook-secret',
}

# Import Jazzmin settings from base settings
from .settings import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS
