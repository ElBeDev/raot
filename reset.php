<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['confirm']) && $_POST['confirm'] === 'reset') {
    header('Content-Type: text/plain');
    echo "Resetting application...\n";
    
    // Run migrations
    echo "Running migrations...\n";
    $output = shell_exec('python3 manage.py migrate --settings=raotproject.production_settings 2>&1');
    echo $output . "\n\n";
    
    // Collect static files
    echo "Collecting static files...\n";
    $output = shell_exec('python3 manage.py collectstatic --noinput --settings=raotproject.production_settings 2>&1');
    echo $output . "\n\n";
    
    // Create superuser
    echo "Creating superuser...\n";
    $password = bin2hex(random_bytes(8)); // Generate random password
    $command = "echo \"from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', '$password')\" | python3 manage.py shell --settings=raotproject.production_settings 2>&1";
    $output = shell_exec($command);
    echo $output . "\n\n";
    
    echo "Reset completed!\n";
    echo "Admin username: admin\n";
    echo "Admin password: $password\n";
    echo "\nIMPORTANT: Login and change this password immediately.";
    echo "\nDELETE THIS FILE AFTER USE!";
    
} else {
?>
<!DOCTYPE html>
<html>
<head>
    <title>Reset Application</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        .warning { background: #ffeeee; border: 1px solid #ff0000; padding: 10px; margin: 20px 0; }
        button { background: #ff0000; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Reset Application</h1>
    
    <div class="warning">
        <h2>WARNING!</h2>
        <p>This will reset your database and potentially cause data loss!</p>
        <p>Only use this for initial setup or if you need to completely reset the application.</p>
    </div>
    
    <form method="post">
        <input type="hidden" name="confirm" value="reset">
        <button type="submit">Yes, Reset Everything</button>
    </form>
</body>
</html>
<?php
}
?>