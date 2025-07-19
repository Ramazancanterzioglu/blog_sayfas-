#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Django setup
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_sayfasi.settings')
django.setup()

from django.conf import settings
from anasayfa.models import DiziFilm

print("=== DJANGO SETUP TEST ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")

# Static dosyalar kontrolü
static_css = Path(settings.STATICFILES_DIRS[0]) / 'css' / 'styles.css'
print(f"CSS Dosyası Var Mı: {static_css.exists()}")
if static_css.exists():
    print(f"CSS Dosyası Boyutu: {static_css.stat().st_size} bytes")

# Model kontrolü
print(f"DiziFilm Modeli: {DiziFilm}")
print(f"DiziFilm Fields: {[field.name for field in DiziFilm._meta.fields]}")

# Template kontrolü
template_dir = Path(settings.TEMPLATES[0]['DIRS'][0])
dizi_template = template_dir / 'anasayfa' / 'dizi-film-onerileri.html'
print(f"Dizi/Film Template Var Mı: {dizi_template.exists()}")

print("\n=== TEST TAMAMLANDI ===")
print("Eğer yukarıdaki bilgiler doğruysa Django kurulumu başarılı!")
print("Sunucuyu başlatmak için: python manage.py runserver") 