<?php
header('Content-Type: text/plain');
echo "Creating superuser...\n";
// The echo command passes "yes" to the stdin of the command to confirm creation
$command = 'echo "yes" | python3 manage.py createsuperuser --noinput --username=admin --email=admin@example.com --settings=raotproject.production_settings 2>&1';
$output = shell_exec($command);
echo $output;
echo "\nAdmin user created with username 'admin'. Use password reset to set password.";
?>