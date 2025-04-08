from pathlib import Path
import os
from .settings import *

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['www.raotsuplementos.com.mx', 'raotsuplementos.com.mx', '69.62.95.109']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store.apps.StoreConfig',
    'cart.apps.CartConfig',
    'checkout.apps.CheckoutConfig',
]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/staticfiles'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/media'

# Email configuration (if needed)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'your-app-password'  # Replace with your app password

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/django_cache',
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# CLIP Payment settings (from your roadmap)
CLIP_API_KEY = 'b8021bcd-4e74-4068-b53b-50c72d4cb80b'
CLIP_SECRET_KEY = '00a1f194-a240-44ad-86e2-ae352679514b'
CLIP_WEBHOOK_SECRET = 'your-webhook-secret'  # Add your webhook secret here
