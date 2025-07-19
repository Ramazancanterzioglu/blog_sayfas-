#!/usr/bin/env bash
set -o errexit

echo "=== RENDER BUILD BAŞLADI ==="
echo "Timestamp: $(date)"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Django version check..."
python -c "import django; print(f'Django {django.get_version()} ready')"

echo "Running Django checks..."
python manage.py check --deploy || echo "⚠️ Django check failed, continuing..."

echo "=== MIGRATION PHASE ==="
echo "Current working directory: $(pwd)"
echo "Python path: $(which python)"

echo "1. Creating migrations if needed..."
python manage.py makemigrations --noinput || echo "⚠️ Makemigrations failed, continuing..."

echo "2. Running initial migration..."
python manage.py migrate --noinput || echo "⚠️ Initial migrate failed, continuing..."

echo "3. Running syncdb (force)..."
python manage.py migrate --run-syncdb --noinput || echo "⚠️ Syncdb failed, continuing..."

echo "4. Final migration attempt..."
python manage.py migrate --noinput || echo "⚠️ Final migrate failed, continuing..."

echo "=== SETUP PHASE ==="
echo "Running full automatic setup..."
python manage.py setup_render || echo "⚠️ Setup render failed, manual setup needed!"

echo "=== VERIFICATION ==="
echo "Testing database tables..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_sayfasi.settings')
django.setup()
from django.db import connection
try:
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\";')
    tables = cursor.fetchall()
    print(f'✅ Database OK - {len(tables)} tables found')
    for table in tables:
        print(f'  - {table[0]}')
except Exception as e:
    print(f'❌ Database verification failed: {str(e)}')
" || echo "⚠️ Database verification failed"

echo "=== STATIC FILES ==="
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "=== BUILD TAMAMLANDI ==="
echo "🎉 Build completed at $(date)"
echo "💡 Check these URLs for status:"
echo "   - /test/ (System status)"
echo "   - /force-migrate/ (Manual migration if needed)"
echo "   - /create-superuser/ (Manual superuser if needed)"
echo "   - /admin/ (Admin panel)" 
