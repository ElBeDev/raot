<?php
header('Content-Type: text/plain');
echo "Sending password reset email...\n";
$output = shell_exec('python3 manage.py changepassword admin --settings=raotproject.production_settings 2>&1');
echo $output;
?>