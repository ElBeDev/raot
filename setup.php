<?php
// Only run on local requests for security
if (!in_array($_SERVER['REMOTE_ADDR'], ['127.0.0.1', '::1']) && 
    strpos($_SERVER['HTTP_HOST'], 'localhost') === false) {
    if (!isset($_GET['confirm']) || $_GET['confirm'] !== 'yes') {
        die("For security, this script requires confirmation. Add ?confirm=yes to the URL if you want to run it.");
    }
}

header('Content-Type: text/plain');
echo "=== RAOT Django Setup ===\n\n";

// Step 1: Create virtual environment
echo "Step 1: Creating virtual environment...\n";
$output = shell_exec('python3 -m venv venv 2>&1');
echo $output . "\n\n";

// Step 2: Install required packages
echo "Step 2: Installing required packages...\n";
$output = shell_exec('./venv/bin/pip install django flup-py3 mysqlclient whitenoise 2>&1');
echo $output . "\n\n";

// Step 3: Make index.fcgi executable
echo "Step 3: Setting permissions...\n";
chmod('index.fcgi', 0755);
echo "Set index.fcgi to 755\n\n";

// Step 4: Run Django migrations
echo "Step 4: Running Django migrations...\n";
$output = shell_exec('./venv/bin/python manage.py migrate --settings=raotproject.production_settings 2>&1');
echo $output . "\n\n";

// Step 5: Collect static files
echo "Step 5: Collecting static files...\n";
$output = shell_exec('./venv/bin/python manage.py collectstatic --noinput --settings=raotproject.production_settings 2>&1');
echo $output . "\n\n";

// Step 6: Create superuser
echo "Step 6: Creating superuser...\n";
$password = bin2hex(random_bytes(8)); // Generate a secure random password
$command = "echo \"from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', '$password')\" | ./venv/bin/python manage.py shell --settings=raotproject.production_settings 2>&1";
$output = shell_exec($command);
echo $output . "\n";
echo "Admin user created with:\n";
echo "Username: admin\n";
echo "Password: $password\n\n";

echo "Setup complete! Remember to delete this file for security.\n";
?>