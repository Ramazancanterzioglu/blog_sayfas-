"""
Render.com deployment için özel Django management command
Bu command otomatik olarak superuser oluşturur ve gerekli kurulumları yapar.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Render.com deployment için otomatik setup'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('🚀 Render.com deployment setup başlatılıyor...')
        )

        # Superuser oluştur
        self.create_superuser()
        
        # Gerekli klasörleri oluştur
        self.create_directories()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Render.com setup tamamlandı!')
        )

    def create_superuser(self):
        """Otomatik superuser oluşturur"""
        
        # Environment variables'dan al, yoksa default değerler
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'ramazancan')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ramazan61135@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345678Ramazan')
        
        try:
            # Eğer kullanıcı zaten varsa kontrol et
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Superuser "{username}" zaten mevcut!')
                )
                user = User.objects.get(username=username)
                
                # Superuser yetkilerini kontrol et ve güncelle
                if not user.is_superuser or not user.is_staff:
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Superuser yetkileri güncellendi!')
                    )
            else:
                # Yeni superuser oluştur
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'🎉 Superuser "{username}" oluşturuldu!')
                )
            
            self.stdout.write(
                self.style.HTTP_INFO(f'📝 Admin Panel: https://yourapp.onrender.com/admin/')
            )
            self.stdout.write(
                self.style.HTTP_INFO(f'👤 Kullanıcı: {username}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Superuser oluşturulurken hata: {str(e)}')
            )

    def create_directories(self):
        """Gerekli klasörleri oluşturur"""
        
        directories = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'dizi_film'),
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.stdout.write(
                    self.style.SUCCESS(f'📁 Klasör oluşturuldu: {directory}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'📁 Klasör zaten mevcut: {directory}')
                ) 