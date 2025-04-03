@echo off
echo Syncing local changes to RAOT server...
scp -r D:\GitHub\raot\static\* root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/static/
ssh root@69.62.95.109 "chown -R www-data:www-data /home/raotsuplementos/htdocs/raotsuplementos.com.mx/static && chmod -R 755 /home/raotsuplementos/htdocs/raotsuplementos.com.mx/static"
echo Sync completed successfully!
