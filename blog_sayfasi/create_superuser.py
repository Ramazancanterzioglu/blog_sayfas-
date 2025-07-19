#!/usr/bin/env python
"""
Otomatik Django Superuser Oluşturma Script'i
Bu script shell etkileşimi olmadan superuser oluşturur.
"""

import os
import sys
import django
from django.core.management.base import BaseCommand

def create_superuser():
    """Otomatik superuser oluşturur"""
    
    # Django setup
    sys.path.append('.')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_sayfasi.settings')
    django.setup()
    
    from django.contrib.auth.models import User
    
    # Superuser bilgileri
    username = 'ramazancan'
    email = 'ramazan61135@gmail.com'
    password = '12345678Ramazan'  # Güvenli bir şifre seçin
    
    try:
        # Eğer kullanıcı zaten varsa kontrol et
        if User.objects.filter(username=username).exists():
            print(f"✅ Superuser '{username}' zaten mevcut!")
            user = User.objects.get(username=username)
            print(f"   Email: {user.email}")
            print(f"   Aktif: {user.is_active}")
            print(f"   Staff: {user.is_staff}")
            print(f"   Superuser: {user.is_superuser}")
        else:
            # Yeni superuser oluştur
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"🎉 Superuser başarıyla oluşturuldu!")
            print(f"   Kullanıcı adı: {username}")
            print(f"   Email: {email}")
            print(f"   Şifre: {password}")
            print(f"   ID: {user.id}")
        
        print("\n📝 Giriş Bilgileri:")
        print(f"   Admin Panel: http://127.0.0.1:8000/admin/")
        print(f"   Kullanıcı adı: {username}")
        print(f"   Şifre: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Superuser oluşturulurken hata: {str(e)}")
        return False

if __name__ == '__main__':
    print("=== DJANGO SUPERUSER OLUŞTURUCU ===")
    success = create_superuser()
    
    if success:
        print("\n✅ İşlem tamamlandı!")
        print("🚀 Artık admin paneline giriş yapabilirsiniz!")
    else:
        print("\n❌ İşlem başarısız!")
        
    print("\n⚠️  NOT: Render'a deploy ederken şifreyi değiştirmeyi unutmayın!") 