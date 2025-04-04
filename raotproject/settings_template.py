"""
PRODUCTION SETTINGS TEMPLATE
Copy this file to settings_local.py on your production server
"""

# Debug should be off in production
DEBUG = False

# Database configuration for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raot_db',
        'USER': 'admin',
        'PASSWORD': 'RaotSuper2025',
        'HOST': 'localhost',  # Changed from IP to localhost for server
        'PORT': '5432',
    }
}

# CLIP.MX Payment Gateway Settings
CLIP_API_KEY = 'f1544953-c525-470c-a912-1f65c11a57ee'
CLIP_SECRET_KEY = 'f254c93d-e7e8-41cf-ab14-a313f3c0d2b3'
CLIP_WEBHOOK_SECRET = 'f254c93d-e7e8-41cf-ab14-a313f3c0d2b3'

# Site URL for production
SITE_URL = 'https://raotsuplementos.com.mx'

# Force production mode for payment processing
FORCE_PRODUCTION = True
FORCE_PAYMENT_SIMULATION = False

# Security settings
ALLOWED_HOSTS = ['raotsuplementos.com.mx', 'www.raotsuplementos.com.mx', '69.62.95.109', 'localhost']

# Static and media settings
STATIC_ROOT = '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/static/collected'
MEDIA_ROOT = '/home/raotsuplementos/htdocs/raotsuplementos.com.mx/media'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP for production