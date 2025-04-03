@echo off
echo Syncing local changes to RAOT server...

echo 1. Uploading Python files...
scp -r D:\GitHub\raot\store\models.py root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/store/
scp -r D:\GitHub\raot\store\admin.py root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/store/
scp -r D:\GitHub\raot\store\templatetags root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/store/

echo 2. Uploading static files...
scp -r D:\GitHub\raot\static\vendor\codemirror root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/static/vendor/
scp -r D:\GitHub\raot\static\js\admin_css_editor.js root@69.62.95.109:/home/raotsuplementos/htdocs/raotsuplementos.com.mx/static/js/

echo 3. Setting permissions and running migrations...
ssh root@69.62.95.109 "cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx && chown -R www-data:www-data . && source venv/bin/activate && python manage.py makemigrations store && python manage.py migrate"

echo 4. Restarting Gunicorn...
ssh root@69.62.95.109 "pkill -f gunicorn && cd /home/raotsuplementos/htdocs/raotsuplementos.com.mx && source venv/bin/activate && gunicorn --bind 127.0.0.1:8001 raotproject.wsgi:application --daemon"

echo Sync completed successfully!
