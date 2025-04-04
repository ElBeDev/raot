"""
Simple server configuration file.
After git pull, run:
python server_config.py
"""

import os
import shutil
import subprocess

# Create settings_local.py with database settings
with open('raotproject/settings_local.py', 'w') as f:
    f.write("""
# Production settings for RAOT Supplements

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raot_db',
        'USER': 'admin',
        'PASSWORD': 'RaotSuper2025',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['raotsuplementos.com.mx', 'www.raotsuplementos.com.mx', '69.62.95.109', 'localhost']

# CLIP.MX Payment Gateway Settings
CLIP_API_KEY = 'f1544953-c525-470c-a912-1f65c11a57ee'
CLIP_SECRET_KEY = 'f254c93d-e7e8-41cf-ab14-a313f3c0d2b3'
CLIP_WEBHOOK_SECRET = 'f254c93d-e7e8-41cf-ab14-a313f3c0d2b3'

# Site URL for production
SITE_URL = 'https://raotsuplementos.com.mx'
""")

# Create necessary directories
os.makedirs('templates/checkout/email', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('media/products', exist_ok=True)

# Activate virtual environment and install requirements
subprocess.run('source venv/bin/activate && pip install -r requirements.txt', shell=True)

# Run migrations
subprocess.run('source venv/bin/activate && python manage.py migrate', shell=True)

# Collect static files
subprocess.run('source venv/bin/activate && python manage.py collectstatic --noinput', shell=True)

# Restart Gunicorn
subprocess.run('tmux send-keys -t raot C-c', shell=True)
subprocess.run('sleep 2', shell=True)
subprocess.run('tmux send-keys -t raot "cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx/ && source venv/bin/activate && gunicorn --bind 127.0.0.1:8090 raotproject.wsgi:application" Enter', shell=True)

print("Setup complete! Your website should be running now.")