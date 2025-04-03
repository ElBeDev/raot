<?php
header('Content-Type: text/plain');
echo "=== RAOT Deployment Debug ===\n\n";

// System info
echo "=== SYSTEM INFO ===\n";
echo "PHP Version: " . phpversion() . "\n";
echo "Server: " . $_SERVER['SERVER_SOFTWARE'] . "\n";
echo "Document Root: " . $_SERVER['DOCUMENT_ROOT'] . "\n\n";

// Python check
echo "=== PYTHON INFO ===\n";
echo "Python path: " . shell_exec('which python3 2>&1') . "\n";
echo "Python version: " . shell_exec('python3 --version 2>&1') . "\n\n";

// Check for wsgi_error.log
echo "=== ERROR LOGS ===\n";
if (file_exists('wsgi_error.log')) {
    echo "WSGI Error Log:\n" . file_get_contents('wsgi_error.log') . "\n\n";
} else {
    echo "No wsgi_error.log found.\n\n";
}

// Check for server error logs
echo "Latest error log entries:\n";
echo shell_exec('tail -n 20 ../logs/error_log 2>&1');
echo "\n\n";

// Project structure
echo "=== PROJECT STRUCTURE ===\n";
echo "Current directory files:\n";
echo shell_exec('ls -la 2>&1') . "\n";
echo "Python files:\n";
echo shell_exec('find . -name "*.py" | head -20 2>&1') . "\n\n";

// Check passenger_wsgi.py content
echo "=== PASSENGER_WSGI.PY CONTENT ===\n";
if (file_exists('passenger_wsgi.py')) {
    echo file_get_contents('passenger_wsgi.py') . "\n\n";
} else {
    echo "passenger_wsgi.py not found!\n\n";
}

// Check database connection
echo "=== DATABASE CONNECTION ===\n";
try {
    $conn = new PDO('mysql:host=localhost;dbname=bernar35_raot_db', 'bernar35_raot_user', 'KiAv5NVA7ZCUQKm');
    echo "Database connection successful!\n";
    
    // Check tables
    $tables = $conn->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);
    echo "Tables found: " . implode(", ", $tables) . "\n";
} catch (PDOException $e) {
    echo "Database connection error: " . $e->getMessage() . "\n";
}
?>