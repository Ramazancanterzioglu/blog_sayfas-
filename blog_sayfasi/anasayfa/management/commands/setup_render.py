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

        # Database kontrolü
        self.check_database()
        
        # Superuser oluştur
        self.create_superuser()
        
        # Gerekli klasörleri oluştur
        self.create_directories()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Render.com setup tamamlandı!')
        )

    def check_database(self):
        """Database bağlantısını ve tabloları kontrol eder"""
        try:
            from django.db import connection
            cursor = connection.cursor()
            
            # Database connection test
            cursor.execute("SELECT 1")
            self.stdout.write(
                self.style.SUCCESS('✅ Database bağlantısı başarılı!')
            )
            
            # Check for auth_user table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            result = cursor.fetchone()
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS('✅ auth_user tablosu mevcut!')
                )
                
                # Count users
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                user_count = cursor.fetchone()[0]
                self.stdout.write(
                    self.style.HTTP_INFO(f'👤 Toplam kullanıcı sayısı: {user_count}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ auth_user tablosu bulunamadı! Migration sorunu olabilir.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Database kontrolü başarısız: {str(e)}')
            )

    def create_superuser(self):
        """Otomatik superuser oluşturur"""
        
        # Environment variables'dan al, yoksa default değerler
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'ramazancan')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ramazan61135@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345678Ramazan')
        
        self.stdout.write(
            self.style.HTTP_INFO(f'🔧 Superuser oluşturma parametreleri:')
        )
        self.stdout.write(f'   Username: {username}')
        self.stdout.write(f'   Email: {email}')
        self.stdout.write(f'   Password length: {len(password)} karakter')
        
        try:
            # Önce mevcut superuser'ları listele
            all_users = User.objects.all()
            self.stdout.write(f'📊 Toplam kullanıcı: {all_users.count()}')
            
            for user in all_users:
                self.stdout.write(f'   - {user.username} (superuser: {user.is_superuser}, staff: {user.is_staff}, active: {user.is_active})')
            
            # Eğer kullanıcı zaten varsa kontrol et
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Superuser "{username}" zaten mevcut!')
                )
                user = User.objects.get(username=username)
                
                # Kullanıcı detaylarını göster
                self.stdout.write(f'📋 Mevcut kullanıcı bilgileri:')
                self.stdout.write(f'   - Username: {user.username}')
                self.stdout.write(f'   - Email: {user.email}')
                self.stdout.write(f'   - Is active: {user.is_active}')
                self.stdout.write(f'   - Is staff: {user.is_staff}')
                self.stdout.write(f'   - Is superuser: {user.is_superuser}')
                self.stdout.write(f'   - Last login: {user.last_login}')
                self.stdout.write(f'   - Date joined: {user.date_joined}')
                
                # Şifreyi güncelle ve yetkileri kontrol et
                user.set_password(password)
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                user.email = email
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superuser "{username}" güncellendi!')
                )
                
                # Şifre testi
                from django.contrib.auth import authenticate
                auth_user = authenticate(username=username, password=password)
                if auth_user:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Şifre doğrulaması başarılı!')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Şifre doğrulaması başarısız!')
                    )
                    
            else:
                # Yeni superuser oluştur
                self.stdout.write(f'🆕 Yeni superuser oluşturuluyor...')
                
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'🎉 Superuser "{username}" oluşturuldu!')
                )
                
                # Oluşturma sonrası kontrol
                user.refresh_from_db()
                self.stdout.write(f'✅ Oluşturulan kullanıcı kontrol:')
                self.stdout.write(f'   - ID: {user.id}')
                self.stdout.write(f'   - Username: {user.username}')
                self.stdout.write(f'   - Is superuser: {user.is_superuser}')
                self.stdout.write(f'   - Is staff: {user.is_staff}')
                self.stdout.write(f'   - Is active: {user.is_active}')
            
            # Final kontrol - tüm superuser'ları listele
            superusers = User.objects.filter(is_superuser=True)
            self.stdout.write(f'🔑 Toplam superuser sayısı: {superusers.count()}')
            for su in superusers:
                self.stdout.write(f'   👑 {su.username} ({su.email})')
            
            self.stdout.write(
                self.style.HTTP_INFO(f'🌐 Admin Panel: https://yourapp.onrender.com/admin/')
            )
            self.stdout.write(
                self.style.HTTP_INFO(f'👤 Kullanıcı: {username}')
            )
            self.stdout.write(
                self.style.HTTP_INFO(f'🔑 Şifre: {password}')
            )
            
        except Exception as e:
            import traceback
            self.stdout.write(
                self.style.ERROR(f'❌ Superuser oluşturulurken hata: {str(e)}')
            )
            self.stdout.write(
                self.style.ERROR(f'🔍 Traceback:\n{traceback.format_exc()}')
            )

    def create_directories(self):
        """Gerekli klasörleri oluşturur"""
        
        directories = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'dizi_film'),
        ]
        
        for directory in directories:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    self.stdout.write(
                        self.style.SUCCESS(f'📁 Klasör oluşturuldu: {directory}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'📁 Klasör zaten mevcut: {directory}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Klasör oluşturulamadı {directory}: {str(e)}')
                ) 