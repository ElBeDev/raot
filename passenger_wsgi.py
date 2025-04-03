import os
import sys

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'raotproject.production_settings'

# Import the WSGI application
from raotproject.wsgi import application