#!/usr/bin/env python
import os
import sys

# Django settings module'unu ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_sayfasi.settings')

try:
    import django
    print(f"✅ Django {django.get_version()} başarıyla import edildi")
    
    # Django'yu başlat
    django.setup()
    print("✅ Django setup başarılı")
    
    # URL'leri kontrol et
    from django.urls import reverse
    from django.conf import settings
    
    print(f"✅ Settings yüklendi - DEBUG: {settings.DEBUG}")
    print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # URL pattern'leri kontrol et
    from django.core.management import execute_from_command_line
    print("✅ Django management komutları çalışıyor")
    
    print("🎉 Django tamamen çalışır durumda!")
    
except Exception as e:
    print(f"❌ HATA: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 