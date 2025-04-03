<?php
header('Content-Type: text/plain');
echo "Collecting static files...\n";
$output = shell_exec('python3 manage.py collectstatic --noinput --settings=raotproject.production_settings 2>&1');
echo $output;
?>