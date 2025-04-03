<?php
header('Content-Type: text/plain');
echo "Running migrations...\n";
$output = shell_exec('python3 manage.py migrate --settings=raotproject.production_settings 2>&1');
echo $output;
?>