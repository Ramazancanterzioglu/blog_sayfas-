"""
Render.com deployment için özel Django management command
Bu command otomatik olarak superuser oluşturur ve gerekli kurulumları yapar.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Render.com deployment için otomatik setup'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('🚀 Render.com FULL SETUP başlatılıyor...')
        )

        # 1. Force migrate first
        self.force_migrate()
        
        # 2. Database kontrolü
        self.check_database()
        
        # 3. Superuser oluştur (force)
        self.force_create_superuser()
        
        # 4. Gerekli klasörleri oluştur
        self.create_directories()
        
        # 5. Final verification
        self.final_verification()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Render.com FULL SETUP tamamlandı!')
        )

    def force_migrate(self):
        """Force migration - tüm migration'ları zorla çalıştır"""
        self.stdout.write(
            self.style.WARNING('🔄 Force migration başlatılıyor...')
        )
        
        try:
            # Run syncdb first
            self.stdout.write('📋 Running migrate --run-syncdb...')
            call_command('migrate', '--run-syncdb', verbosity=1)
            
            # Run normal migrations
            self.stdout.write('📋 Running normal migrations...')
            call_command('migrate', verbosity=1)
            
            # Make sure all apps are migrated
            self.stdout.write('📋 Running makemigrations...')
            call_command('makemigrations', verbosity=1)
            
            # Final migrate
            self.stdout.write('📋 Final migration...')
            call_command('migrate', verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Force migration tamamlandı!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Migration hatası: {str(e)}')
            )
            # Continue anyway
            
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
            
            # List all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            self.stdout.write(f'📊 Database tables ({len(tables)}):')
            for table in tables:
                self.stdout.write(f'  - {table}')
            
            # Check critical tables
            critical_tables = ['auth_user', 'anasayfa_dizifilm', 'anasayfa_geziblog']
            for table in critical_tables:
                if table in tables:
                    self.stdout.write(f'✅ {table} tablosu mevcut')
                else:
                    self.stdout.write(f'⚠️ {table} tablosu eksik')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Database kontrolü başarısız: {str(e)}')
            )

    def force_create_superuser(self):
        """Force superuser oluştur - aggressive mode"""
        
        # Environment variables'dan al, yoksa default değerler
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'ramazancan')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ramazan61135@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345678Ramazan')
        
        self.stdout.write(
            self.style.WARNING(f'🔧 FORCE Superuser oluşturma: {username}')
        )
        
        try:
            # Delete existing user if exists (aggressive approach)
            existing_users = User.objects.filter(username=username)
            if existing_users.exists():
                existing_users.delete()
                self.stdout.write(f'🗑️ Mevcut kullanıcı silindi: {username}')
            
            # Create fresh superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            # Double check permissions
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'🎉 FORCE Superuser oluşturuldu: {username}')
            )
            
            # Test authentication
            from django.contrib.auth import authenticate
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                self.stdout.write(f'✅ Authentication test başarılı!')
            else:
                self.stdout.write(f'❌ Authentication test başarısız!')
            
            # Final superuser count
            superuser_count = User.objects.filter(is_superuser=True).count()
            self.stdout.write(f'👑 Toplam superuser: {superuser_count}')
            
            self.stdout.write(f'🔑 LOGIN INFO:')
            self.stdout.write(f'   Username: {username}')
            self.stdout.write(f'   Password: {password}')
            self.stdout.write(f'   Admin URL: /admin/')
            
        except Exception as e:
            import traceback
            self.stdout.write(
                self.style.ERROR(f'❌ FORCE Superuser hatası: {str(e)}')
            )
            self.stdout.write(f'🔍 Traceback:\n{traceback.format_exc()}')

    def create_directories(self):
        """Gerekli klasörleri oluşturur"""
        
        directories = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'dizi_film'),
            os.path.join(settings.MEDIA_ROOT, 'gezi_blog'),
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

    def final_verification(self):
        """Final doğrulama - her şeyin çalıştığını kontrol et"""
        self.stdout.write(
            self.style.WARNING('🔍 Final verification başlatılıyor...')
        )
        
        try:
            # User count
            total_users = User.objects.count()
            superusers = User.objects.filter(is_superuser=True).count()
            
            # Model counts
            from anasayfa.models import DiziFilm, GeziBlog
            dizi_count = DiziFilm.objects.count()
            gezi_count = GeziBlog.objects.count()
            
            # Summary
            self.stdout.write(f'📊 FINAL STATS:')
            self.stdout.write(f'   👤 Total users: {total_users}')
            self.stdout.write(f'   👑 Superusers: {superusers}')
            self.stdout.write(f'   🎬 DiziFilm records: {dizi_count}')
            self.stdout.write(f'   🗺️ GeziBlog records: {gezi_count}')
            self.stdout.write(f'   📁 Media root: {settings.MEDIA_ROOT}')
            
            # Test critical functionality
            if superusers > 0:
                self.stdout.write('✅ Superuser check: PASSED')
            else:
                self.stdout.write('❌ Superuser check: FAILED')
                
            # Test models
            try:
                DiziFilm.objects.all().exists()
                self.stdout.write('✅ DiziFilm model: WORKING')
            except Exception:
                self.stdout.write('❌ DiziFilm model: ERROR')
                
            try:
                GeziBlog.objects.all().exists()
                self.stdout.write('✅ GeziBlog model: WORKING')
            except Exception:
                self.stdout.write('❌ GeziBlog model: ERROR')
                
            self.stdout.write(
                self.style.SUCCESS('✅ Final verification tamamlandı!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Final verification hatası: {str(e)}')
            ) 