#!/bin/bash

# Create Gunicorn start script
cat > run_gunicorn.sh << EOF
#!/bin/bash
cd /var/www/raotsuplementos.com.mx
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=raotproject.production_settings
exec gunicorn raotproject.wsgi:application --bind 127.0.0.1:8000 --workers=3
EOF

chmod +x run_gunicorn.sh

# Create systemd service
cat > /etc/systemd/system/gunicorn-raot.service << EOF
[Unit]
Description=Gunicorn daemon for RAOT Supplements
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/raotsuplementos.com.mx
ExecStart=/var/www/raotsuplementos.com.mx/run_gunicorn.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable gunicorn-raot
systemctl restart gunicorn-raot