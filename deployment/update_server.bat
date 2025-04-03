@echo off
echo Syncing local changes to RAOT server...
scp -r D:\GitHub\raot\static\* root@69.62.95.109:/home/raotsuplementos/htdocs/raotsu# Create the deployment directory if needed
New-Item -Path "D:\GitHub\raot\deployment" -ItemType Directory -Force

# Create update_server.bat
@'
@echo off
echo Updating RAOT server...
ssh root@69.62.95.109 "cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx && git pull"
echo Server updated successfully!
