from .settings import *

DEBUG = True

# Remote database connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raot_db',
        'USER': 'admin',
        'PASSWORD': 'RaotSuper2025',
        'HOST': '69.62.95.109',
        'PORT': '5432',
    }
}

# Development settings
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
STATIC_URL = '/static/'
MEDIA_URL = '/media/'