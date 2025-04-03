#!/bin/bash
cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=raotproject.production_settings
exec gunicorn raotproject.wsgi:application --bind 127.0.0.1:8090 --workers 3
