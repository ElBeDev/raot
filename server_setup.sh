#!/bin/bash

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Set up database
mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS roat;
CREATE USER IF NOT EXISTS 'bener'@'localhost' IDENTIFIED BY 'hR0VOwz8tqa1mtMkdHMB';
GRANT ALL PRIVILEGES ON roat.* TO 'bener'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

# Run Django commands
python manage.py migrate --settings=raotproject.production_settings
python manage.py collectstatic --noinput --settings=raotproject.production_settings
python manage.py createsuperuser --settings=raotproject.production_settings