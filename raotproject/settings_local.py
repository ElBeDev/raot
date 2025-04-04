from .settings import *

# RENAME THIS FILE TO settings_local.py on the server

# This file should only override specific settings from settings.py

# Make sure you have DEBUG enabled
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use the correct PostgreSQL connection parameters
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raot_db',
        'USER': 'admin',
        'PASSWORD': 'RaotSuper2025',  # Corrected password with lowercase 'a'
        'HOST': '69.62.95.109',
        'PORT': '5432',
    }
}

# Enable detailed logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Important: Make sure you're not overriding INSTALLED_APPS or MIDDLEWARE
# These should typically stay in the main settings.py