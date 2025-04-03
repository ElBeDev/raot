from .settings import *
import os

# Security settings
DEBUG = False
SECRET_KEY = '@1p*qx(zr&l=0q_6@ls@w7^=!bv47_l%t43@morai&=8o3v&3g'

# Hostinger domain settings
ALLOWED_HOSTS = ['raotsuplementos.com.mx', 'www.raotsuplementos.com.mx']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roat',
        'USER': 'bener',
        'PASSWORD': 'hR0VOwz8tqa1mtMkdHMB',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files (User uploaded content)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# WhiteNoise for static files
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    security_index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    MIDDLEWARE.insert(security_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Email settings - update for Hostinger
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@raotsuplementos.com.mx'  # Update with your actual email
EMAIL_HOST_PASSWORD = 'your-email-password'  # Update with your actual password