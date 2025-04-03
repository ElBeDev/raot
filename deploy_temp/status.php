<?php
header('Content-Type: text/plain');
echo "=== RAOT Django Status Check ===\n\n";

// Check Python version
echo "Python version:\n";
$output = shell_exec('python3 -V 2>&1');
echo $output . "\n";

// Check if index.fcgi exists and is executable
echo "index.fcgi status: ";
if (file_exists('index.fcgi')) {
    $perms = substr(sprintf('%o', fileperms('index.fcgi')), -4);
    echo "Exists (permissions: $perms)\n";
} else {
    echo "MISSING!\n";
}

// Check virtual environment
echo "Virtual environment: ";
if (is_dir('venv')) {
    echo "Exists\n";
} else {
    echo "Not found\n";
}

// Check .htaccess
echo ".htaccess status: ";
if (file_exists('.htaccess')) {
    echo "Exists\n";
} else {
    echo "MISSING!\n";
}

// Check logs
echo "\nRecent error logs:\n";
if (file_exists('django_error.log')) {
    $output = shell_exec('tail -n 20 django_error.log 2>&1');
    echo $output . "\n";
} else {
    echo "No django_error.log found\n";
}

// Try to access Django
echo "\nTrying to access Django via command line:\n";
$output = shell_exec('DJANGO_SETTINGS_MODULE=raotproject.production_settings python3 -c "import django; print(django.get_version())" 2>&1');
echo $output . "\n";

echo "\nStatus check complete.\n";
?>