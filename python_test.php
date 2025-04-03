<?php
header('Content-Type: text/plain');
echo "Testing Python execution...\n\n";

// Try multiple Python paths
$pythonPaths = ['python3', 'python', '/usr/bin/python3', '/usr/bin/python'];

foreach ($pythonPaths as $pythonPath) {
    echo "Testing $pythonPath:\n";
    $result = shell_exec("$pythonPath -V 2>&1");
    if ($result) {
        echo "SUCCESS: $result\n";
    } else {
        echo "FAILED: No output\n";
    }
    echo "\n";
}

// Check file permissions
echo "File permissions:\n";
echo "test_wsgi.py: " . substr(sprintf('%o', fileperms('test_wsgi.py')), -4) . "\n";
echo "passenger_wsgi.py: " . substr(sprintf('%o', fileperms('passenger_wsgi.py')), -4) . "\n";
echo ".htaccess: " . substr(sprintf('%o', fileperms('.htaccess')), -4) . "\n";

// Check if Python can run as CGI
echo "\nTesting CGI execution capability:\n";
$cgiTest = '#!/usr/bin/env python3
print("Content-Type: text/plain\\n")
print("Python CGI is working!")';

file_put_contents('cgi_test.py', $cgiTest);
chmod('cgi_test.py', 0755);

echo "Created test CGI file with permissions: " . substr(sprintf('%o', fileperms('cgi_test.py')), -4) . "\n";
echo "Visit: https://raotsuplementos.com.mx/cgi_test.py to test direct CGI execution\n";
?>