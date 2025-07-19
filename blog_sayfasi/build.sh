#!/usr/bin/env bash
set -o errexit

echo "=== RENDER BUILD BAŞLADI ==="

echo "Current directory:"
pwd

echo "Environment variables:"
echo "RENDER: $RENDER"
echo "DEBUG: $DEBUG"

echo "Python version:"
python --version

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Django version:"
python -c "import django; print(django.get_version())"

echo "Current working directory contents:"
ls -la

echo "Database directory permissions:"
ls -la /tmp/

echo "Testing Django setup..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_sayfasi.settings')
import django
django.setup()
from django.conf import settings
print(f'Database ENGINE: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
print(f'Database NAME: {settings.DATABASES[\"default\"][\"NAME\"]}')
print(f'INSTALLED_APPS: {settings.INSTALLED_APPS}')
"

echo "Checking Django project..."
python manage.py check

echo "Showing available migrations..."
python manage.py showmigrations

echo "Force creating migrations if needed..."
python manage.py makemigrations --noinput

echo "Running migrations with verbose output..."
python manage.py migrate --noinput --verbosity=2

echo "Migration status after migrate:"
python manage.py showmigrations

echo "Testing database tables..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_sayfasi.settings')
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\";')
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(f'  - {table[0]}')
"

echo "Creating superuser if needed..."
echo "Setting up Render environment..."
python manage.py setup_render

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "=== BUILD TAMAMLANDI ===" 
