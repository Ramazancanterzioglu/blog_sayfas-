#!/usr/bin/env bash
set -o errexit

echo "=== BUILD BAŞLADI ==="

echo "Python version:"
python --version

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Django version:"
python -c "import django; print(django.get_version())"

echo "Checking Django project..."
python manage.py check

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running migrations..."
python manage.py migrate

echo "=== BUILD TAMAMLANDI ===" 
