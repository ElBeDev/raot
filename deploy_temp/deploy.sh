#!/bin/bash

# Run the server setup script
bash server_setup.sh

# Set up Gunicorn
bash setup_gunicorn.sh

# Set up Nginx
bash setup_nginx.sh

# Fix permissions
bash fix_permissions.sh

echo "Deployment complete! RAOT Supplements website should be live."
echo "Visit: http://raotsuplementos.com.mx/"