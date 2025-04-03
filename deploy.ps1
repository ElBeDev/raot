# Define source and destination
$source = "D:\GitHub\raot"
$destination = "root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/"

# Clean Python cache files
Write-Host "Cleaning Python cache files..."
Get-ChildItem -Path "$source" -Include "*.pyc","*.pyo" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "$source" -Include "__pycache__" -Directory -Recurse | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Remove IDE files
Write-Host "Removing IDE files..."
Remove-Item -Path "$source\.vscode" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$source\.idea" -Recurse -Force -ErrorAction SilentlyContinue

# Remove log files
Write-Host "Removing log files..."
Get-ChildItem -Path "$source" -Include "*.log" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue

# Upload files using SCP
Write-Host "Uploading files to server..."
scp -r "${source}\*" $destination

# Connect and run necessary setup commands
Write-Host "Setting up virtual environment and running migrations..."
ssh root@69.62.95.109 "cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py collectstatic --noinput --clear && python manage.py migrate"

# Restart Gunicorn
Write-Host "Restarting Gunicorn..."
ssh root@69.62.95.109 "pkill gunicorn || true && tmux new-session -d -s raot 'cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx && source venv/bin/activate && gunicorn --bind 127.0.0.1:8001 raotproject.wsgi:application'"

Write-Host "Deployment complete! Visit https://raotsuplementos.com.mx"
