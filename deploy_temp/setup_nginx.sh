#!/bin/bash

# Create Nginx site configuration
cat > /etc/nginx/sites-available/raotsuplementos.com.mx << EOF
server {
    listen 80;
    server_name raotsuplementos.com.mx www.raotsuplementos.com.mx;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/raotsuplementos.com.mx;
    }
    
    location /media/ {
        root /var/www/raotsuplementos.com.mx;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

# Create proxy_params if it doesn't exist
if [ ! -f "/etc/nginx/proxy_params" ]; then
    cat > /etc/nginx/proxy_params << EOF
proxy_set_header Host \$http_host;
proxy_set_header X-Real-IP \$remote_addr;
proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto \$scheme;
EOF
fi

# Enable the site
ln -sf /etc/nginx/sites-available/raotsuplementos.com.mx /etc/nginx/sites-enabled/

# Remove default site if it exists
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    rm -f /etc/nginx/sites-enabled/default
fi

# Test and restart Nginx
nginx -t
systemctl restart nginx