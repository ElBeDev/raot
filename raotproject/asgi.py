"""
ASGI config for raotproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Make sure it's using the main settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raotproject.settings')
application = get_asgi_application()
