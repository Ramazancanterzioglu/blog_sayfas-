#!/usr/bin/env bash
set -o errexit

echo "=== RENDER BUILD BAŞLADI ==="

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Django version check..."
python -c "import django; print(f'Django {django.get_version()} ready')"

echo "Running Django checks..."
python manage.py check --deploy

echo "FULL AUTOMATIC SETUP - Migration + Superuser..."
python manage.py setup_render

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "=== BUILD TAMAMLANDI ==="
echo "🎉 Site ready! Admin: /admin/ - User: ramazancan" 
