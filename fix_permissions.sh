#!/bin/bash

# Set ownership
chown -R www-data:www-data /var/www/raotsuplementos.com.mx/

# Set permissions
find /var/www/raotsuplementos.com.mx -type d -exec chmod 755 {} \;
find /var/www/raotsuplementos.com.mx -type f -exec chmod 644 {} \;

# Make scripts executable
chmod +x /var/www/raotsuplementos.com.mx/*.sh
chmod +x /var/www/raotsuplementos.com.mx/manage.py

# Ensure media and static directories are writable
mkdir -p /var/www/raotsuplementos.com.mx/media
mkdir -p /var/www/raotsuplementos.com.mx/staticfiles
chmod -R 775 /var/www/raotsuplementos.com.mx/media
chmod -R 775 /var/www/raotsuplementos.com.mx/staticfiles