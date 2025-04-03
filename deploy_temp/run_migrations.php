<?php
header('Content-Type: text/plain');
echo "Running Django migrations...\n\n";

// First try Python 3
$output = shell_exec('python3 manage.py migrate --settings=raotproject.production_settings 2>&1');

// If that fails, try plain Python
if (!$output) {
    $output = shell_exec('python manage.py migrate --settings=raotproject.production_settings 2>&1');
}

echo $output;

// Create a superuser
echo "\n\nCreating superuser...\n";
$password = bin2hex(random_bytes(8)); // Generate random secure password

$command = "echo \"from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', '$password')\" | python3 manage.py shell --settings=raotproject.production_settings 2>&1";
$output = shell_exec($command);

echo $output;
echo "\n\nAdmin user created with:\n";
echo "Username: admin\n";
echo "Password: $password\n";
?>