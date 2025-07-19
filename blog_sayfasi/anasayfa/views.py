from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import DiziFilm, GeziBlog
import os
from django.db import models

def anasayfa(request):
    # Debug için template path kontrolü
    template_path = 'anasayfa/index.html'
    try:
        return render(request, template_path)
    except Exception as e:
        if settings.DEBUG:
            return HttpResponse(f"""
            <h1>Debug Bilgisi</h1>
            <p>Template Hatası: {str(e)}</p>
            <p>Template Path: {template_path}</p>
            <p>TEMPLATE_DIRS: {settings.TEMPLATES[0]['DIRS']}</p>
            <p>BASE_DIR: {settings.BASE_DIR}</p>
            <p>Template files:</p>
            <ul>
            """)
        raise

def oran_analizleri(request):
    return render(request, 'anasayfa/oran-analizleri.html')

def muhasebe_terimleri(request):
    return render(request, 'anasayfa/muhasebe-terimleri.html')

def dizi_film_onerileri(request):
    try:
        # Tüm önerilen dizi/filmleri getir
        dizi_filmler = DiziFilm.objects.filter(onerilen=True).order_by('-olusturma_tarihi')
        
        # Kategori filtreleme
        kategori = request.GET.get('kategori')
        if kategori:
            dizi_filmler = dizi_filmler.filter(kategori=kategori)
        
        # Tür filtreleme
        tur = request.GET.get('tur')
        if tur:
            dizi_filmler = dizi_filmler.filter(tur=tur)
        
        # Arama
        arama = request.GET.get('arama')
        if arama:
            dizi_filmler = dizi_filmler.filter(isim__icontains=arama)
        
        context = {
            'dizi_filmler': dizi_filmler,
            'kategori_choices': DiziFilm.KATEGORI_CHOICES,
            'tur_choices': DiziFilm.TUR_CHOICES,
            'secili_kategori': kategori,
            'secili_tur': tur,
            'arama_terimi': arama,
        }
        
        return render(request, 'anasayfa/dizi-film-onerileri.html', context)
        
    except Exception as e:
        from django.conf import settings
        import traceback
        
        error_details = f"""
        <h1>🔍 Dizi/Film Önerileri Debug</h1>
        <h2>Hata Detayları:</h2>
        <p><strong>Hata:</strong> {str(e)}</p>
        <p><strong>Hata Türü:</strong> {type(e).__name__}</p>
        
        <h3>Traceback:</h3>
        <pre style="background: #f5f5f5; padding: 1rem; overflow: auto;">
{traceback.format_exc()}
        </pre>
        
        <h3>Database Test:</h3>
        """
        
        # Database test
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anasayfa_dizifilm';")
            table_exists = cursor.fetchone()
            
            if table_exists:
                error_details += "<p>✅ anasayfa_dizifilm tablosu mevcut</p>"
                try:
                    DiziFilm.objects.count()
                    error_details += "<p>✅ DiziFilm model'i çalışıyor</p>"
                except Exception as model_e:
                    error_details += f"<p>❌ DiziFilm model hatası: {str(model_e)}</p>"
            else:
                error_details += "<p>❌ anasayfa_dizifilm tablosu yok - migration gerekli</p>"
                
        except Exception as db_e:
            error_details += f"<p>❌ Database test hatası: {str(db_e)}</p>"
        
        error_details += """
        <hr>
        <p><a href="/test/">System Test</a> | <a href="/">Ana Sayfa</a></p>
        """
        
        if settings.DEBUG:
            return HttpResponse(error_details)
        else:
            # Production'da generic error page
            return render(request, 'anasayfa/index.html', {
                'error_message': 'Dizi/Film önerileri yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.'
            })

def dizi_film_detay(request, pk):
    try:
        dizi_film = get_object_or_404(DiziFilm, pk=pk)
        # Benzer öneriler (aynı tür veya kategori)
        benzer_oneriler = DiziFilm.objects.filter(
            onerilen=True
        ).filter(
            tur=dizi_film.tur
        ).exclude(
            pk=dizi_film.pk
        )[:3]
        
        context = {
            'dizi_film': dizi_film,
            'benzer_oneriler': benzer_oneriler,
        }
        
        return render(request, 'anasayfa/dizi-film-detay.html', context)
        
    except DiziFilm.DoesNotExist:
        from django.conf import settings
        if settings.DEBUG:
            return HttpResponse(f"""
            <h1>Dizi/Film Bulunamadı</h1>
            <p>ID: {pk} olan dizi/film bulunamadı.</p>
            <p><a href="/dizi-film-onerileri/">Dizi/Film Önerileri</a></p>
            <p><a href="/">Ana Sayfa</a></p>
            """)
        else:
            return render(request, 'anasayfa/dizi-film-onerileri.html', {
                'error_message': 'Aradığınız içerik bulunamadı.'
            })
    except Exception as e:
        from django.conf import settings
        if settings.DEBUG:
            return HttpResponse(f"""
            <h1>Dizi/Film Detay Sayfası Hatası</h1>
            <p><strong>Hata:</strong> {str(e)}</p>
            <p><strong>Hata Türü:</strong> {type(e).__name__}</p>
            <p><strong>ID:</strong> {pk}</p>
            <hr>
            <p><a href="/dizi-film-onerileri/">Dizi/Film Önerileri</a></p>
            <p><a href="/">Ana Sayfa</a></p>
            """)
        else:
            return render(request, 'anasayfa/dizi-film-onerileri.html', {
                'error_message': 'İçerik yüklenirken bir hata oluştu.'
            })

def gezi_blog_onerileri(request):
    try:
        # Tüm önerilen gezi bloglarını getir
        gezi_bloglari = GeziBlog.objects.filter(onerilen=True).order_by('-olusturma_tarihi')
        
        # Kategori filtreleme
        kategori = request.GET.get('kategori')
        if kategori:
            gezi_bloglari = gezi_bloglari.filter(kategori=kategori)
        
        # Şehir filtreleme
        sehir = request.GET.get('sehir')
        if sehir:
            gezi_bloglari = gezi_bloglari.filter(sehir__icontains=sehir)
        
        # Puan filtreleme
        puan = request.GET.get('puan')
        if puan:
            gezi_bloglari = gezi_bloglari.filter(puanim__gte=puan)
        
        # Arama
        arama = request.GET.get('arama')
        if arama:
            gezi_bloglari = gezi_bloglari.filter(
                models.Q(yer_adi__icontains=arama) | 
                models.Q(sehir__icontains=arama) |
                models.Q(kisa_aciklama__icontains=arama)
            )
        
        # Şehirler listesi (filtreleme için)
        sehirler = GeziBlog.objects.filter(onerilen=True).values_list('sehir', flat=True).distinct().order_by('sehir')
        
        context = {
            'gezi_bloglari': gezi_bloglari,
            'kategori_choices': GeziBlog.KATEGORI_CHOICES,
            'puan_choices': GeziBlog.PUAN_CHOICES,
            'sehirler': sehirler,
            'secili_kategori': kategori,
            'secili_sehir': sehir,
            'secili_puan': puan,
            'arama_terimi': arama,
        }
        
        return render(request, 'anasayfa/gezi-blog-onerileri.html', context)
        
    except Exception as e:
        from django.conf import settings
        import traceback
        
        error_details = f"""
        <h1>🗺️ Gezi Blog Önerileri Debug</h1>
        <h2>Hata Detayları:</h2>
        <p><strong>Hata:</strong> {str(e)}</p>
        <p><strong>Hata Türü:</strong> {type(e).__name__}</p>
        
        <h3>Traceback:</h3>
        <pre style="background: #f5f5f5; padding: 1rem; overflow: auto;">
{traceback.format_exc()}
        </pre>
        
        <h3>Database Test:</h3>
        """
        
        # Database test
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anasayfa_geziblog';")
            table_exists = cursor.fetchone()
            
            if table_exists:
                error_details += "<p>✅ anasayfa_geziblog tablosu mevcut</p>"
                try:
                    GeziBlog.objects.count()
                    error_details += "<p>✅ GeziBlog model'i çalışıyor</p>"
                except Exception as model_e:
                    error_details += f"<p>❌ GeziBlog model hatası: {str(model_e)}</p>"
            else:
                error_details += "<p>❌ anasayfa_geziblog tablosu yok - migration gerekli</p>"
                
        except Exception as db_e:
            error_details += f"<p>❌ Database test hatası: {str(db_e)}</p>"
        
        error_details += """
        <hr>
        <p><a href="/test/">System Test</a> | <a href="/">Ana Sayfa</a></p>
        """
        
        if settings.DEBUG:
            return HttpResponse(error_details)
        else:
            # Production'da generic error page
            return render(request, 'anasayfa/index.html', {
                'error_message': 'Gezi blog önerileri yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.'
            })

def gezi_blog_detay(request, pk):
    try:
        gezi_blog = get_object_or_404(GeziBlog, pk=pk)
        # Benzer öneriler (aynı şehir veya kategori)
        benzer_oneriler = GeziBlog.objects.filter(
            onerilen=True
        ).filter(
            models.Q(sehir=gezi_blog.sehir) | models.Q(kategori=gezi_blog.kategori)
        ).exclude(
            pk=gezi_blog.pk
        )[:3]
        
        context = {
            'gezi_blog': gezi_blog,
            'benzer_oneriler': benzer_oneriler,
        }
        
        return render(request, 'anasayfa/gezi-blog-detay.html', context)
        
    except GeziBlog.DoesNotExist:
        from django.conf import settings
        if settings.DEBUG:
            return HttpResponse(f"""
            <h1>Gezi Blog Bulunamadı</h1>
            <p>ID: {pk} olan gezi blog bulunamadı.</p>
            <p><a href="/gezi-blog-onerileri/">Gezi Blog Önerileri</a></p>
            <p><a href="/">Ana Sayfa</a></p>
            """)
        else:
            return render(request, 'anasayfa/gezi-blog-onerileri.html', {
                'error_message': 'Aradığınız gezi blogu bulunamadı.'
            })
    except Exception as e:
        from django.conf import settings
        if settings.DEBUG:
            return HttpResponse(f"""
            <h1>Gezi Blog Detay Sayfası Hatası</h1>
            <p><strong>Hata:</strong> {str(e)}</p>
            <p><strong>Hata Türü:</strong> {type(e).__name__}</p>
            <p><strong>ID:</strong> {pk}</p>
            <hr>
            <p><a href="/gezi-blog-onerileri/">Gezi Blog Önerileri</a></p>
            <p><a href="/">Ana Sayfa</a></p>
            """)
        else:
            return render(request, 'anasayfa/gezi-blog-onerileri.html', {
                'error_message': 'İçerik yüklenirken bir hata oluştu.'
            })

def ornek_sayfa(request):
    return render(request, 'anasayfa/ornek.html')

# Debug için basit test view
def test_view(request):
    import django
    import sys
    from django.db import connection
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    
    # Database test
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        db_status = f"✅ Database OK - {len(tables)} tables"
        
        # User test
        try:
            user_count = User.objects.count()
            user_status = f"✅ Users: {user_count}"
            
            if user_count > 0:
                users = User.objects.all()[:5]
                user_list = []
                for u in users:
                    user_info = f"{u.username} - Staff: {u.is_staff}, Super: {u.is_superuser}, Active: {u.is_active}"
                    user_list.append(user_info)
                user_details = "<br>".join(user_list)
                
                # Test superuser authentication
                superusers = User.objects.filter(is_superuser=True)
                auth_test = "<h3>🔐 Superuser Authentication Test:</h3>"
                
                for su in superusers:
                    # Try common passwords
                    test_passwords = ['12345678Ramazan', 'admin', 'password']
                    for pwd in test_passwords:
                        auth_user = authenticate(username=su.username, password=pwd)
                        if auth_user:
                            auth_test += f"<p>✅ {su.username} + {pwd} = SUCCESS</p>"
                            break
                    else:
                        auth_test += f"<p>❌ {su.username} - PASSWORD NOT FOUND in test list</p>"
                        
            else:
                user_details = "No users found"
                auth_test = ""
                
        except Exception as e:
            user_status = f"❌ User error: {str(e)}"
            user_details = ""
            auth_test = ""
            
    except Exception as e:
        db_status = f"❌ Database error: {str(e)}"
        tables = []
        user_status = "❌ Can't check users"
        user_details = ""
        auth_test = ""
    
    # DiziFilm test
    try:
        from .models import DiziFilm
        dizi_count = DiziFilm.objects.count()
        dizi_status = f"✅ DiziFilm: {dizi_count} items"
    except Exception as e:
        dizi_status = f"❌ DiziFilm error: {str(e)}"
    
    # Environment info
    env_info = f"""
    <h3>🌍 Environment:</h3>
    <ul>
        <li>RENDER: {os.environ.get('RENDER', 'Not set')}</li>
        <li>DEBUG: {settings.DEBUG}</li>
        <li>Database: {settings.DATABASES['default']['ENGINE']}</li>
        <li>Database Name: {settings.DATABASES['default']['NAME']}</li>
        <li>DJANGO_SUPERUSER_USERNAME: {os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Not set')}</li>
        <li>DJANGO_SUPERUSER_EMAIL: {os.environ.get('DJANGO_SUPERUSER_EMAIL', 'Not set')}</li>
        <li>Password Length: {len(os.environ.get('DJANGO_SUPERUSER_PASSWORD', ''))}</li>
    </ul>
    """
    
    return HttpResponse(f"""
    <h1>🎉 Django Çalışıyor!</h1>
    <h2>Sistem Bilgileri:</h2>
    <ul>
        <li>Django Version: {django.get_version()}</li>
        <li>Python Version: {sys.version}</li>
        <li>Debug Mode: {settings.DEBUG}</li>
        <li>Allowed Hosts: {settings.ALLOWED_HOSTS}</li>
    </ul>
    
    {env_info}
    
    <h2>Database Durumu:</h2>
    <ul>
        <li>{db_status}</li>
        <li>{user_status}</li>
        <li>{dizi_status}</li>
    </ul>
    
    <h3>Database Tables:</h3>
    <ul>
        {''.join([f'<li>{table}</li>' for table in tables])}
    </ul>
    
    <h3>Users:</h3>
    <p>{user_details}</p>
    
    {auth_test}
    
    <h2>Manual Superuser Creation:</h2>
    <p><a href="/create-superuser/" style="background: #007cba; color: white; padding: 10px; text-decoration: none;">🔑 Create/Update Superuser (BACKUP)</a></p>
    
    <h2>⚙️ Migration & Setup Status:</h2>
    <div style="background: #e7f3ff; color: #004085; padding: 15px; border-radius: 5px; border: 1px solid #b3d7ff; margin: 10px 0;">
        <h3>🔄 Çift Sistem Aktif:</h3>
        <p><strong>1. Otomatik Setup:</strong> Build sırasında çalışır (setup_render command)</p>
        <ul>
            <li>✅ Otomatik migration</li>
            <li>✅ Otomatik superuser</li>
            <li>✅ Media klasörleri</li>
        </ul>
        <p><strong>2. Manuel Backup:</strong> Otomatik başarısız olursa</p>
        <ul>
            <li>🔧 Manuel migration → <a href="/force-migrate/">Force Migrate</a></li>
            <li>🔧 Manuel superuser → <a href="/create-superuser/">Create Superuser</a></li>
        </ul>
        <p><strong>Önce otomatik denenir, başarısız olursa manuel kullanın!</strong></p>
    </div>
    
    <h2>Media Files Test:</h2>
    <p><a href="/media-test/" style="background: #28a745; color: white; padding: 10px; text-decoration: none;">📁 Media Files Debug</a></p>
    
    <h2>Test Linkleri:</h2>
    <ul>
        <li><a href="/">Ana Sayfa</a></li>
        <li><a href="/oran-analizleri/">Oran Analizleri</a></li>
        <li><a href="/muhasebe-terimleri/">Muhasebe Terimleri</a></li>
        <li><a href="/dizi-film-onerileri/">Dizi/Film Önerileri</a></li>
        <li><a href="/gezi-blog-onerileri/">Gezi Blog Önerileri</a></li>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/force-migrate/">🚨 Force Migrate (BACKUP)</a></li>
    </ul>
    """)

def force_migrate(request):
    """Manuel migration - Backup çözüm"""
    from django.core.management import call_command
    from io import StringIO
    import sys
    
    html_output = f"""
    <h1>🚨 Force Migration - Manuel Backup</h1>
    
    <div style="background: #fff3cd; color: #856404; padding: 20px; border-radius: 10px; border: 1px solid #ffeaa7; margin: 20px 0;">
        <h2>⚠️ Migration Backup Tool</h2>
        <p><strong>Otomatik migration çalışmadıysa bu sayfayı kullanın!</strong></p>
        <p>Bu sayfa migration'ları zorla çalıştırır ve database'i düzeltir.</p>
    </div>
    """
    
    # Migration işlemi başlat
    if request.method == 'GET' and 'run' in request.GET:
        html_output += "<h2>🔄 Migration İşlemi Başlatılıyor...</h2>"
        html_output += "<pre style='background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;'>"
        
        output = StringIO()
        
        try:
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = output
            
            # 1. Makemigrations
            print("=== 1. MAKEMIGRATIONS ===")
            try:
                call_command('makemigrations', '--noinput', verbosity=2)
                print("✅ Makemigrations başarılı")
            except Exception as e:
                print(f"⚠️ Makemigrations hatası: {str(e)}")
            
            # 2. Normal migrate
            print("\n=== 2. NORMAL MIGRATE ===")
            try:
                call_command('migrate', '--noinput', verbosity=2)
                print("✅ Normal migrate başarılı")
            except Exception as e:
                print(f"⚠️ Normal migrate hatası: {str(e)}")
            
            # 3. Syncdb migrate
            print("\n=== 3. SYNCDB MIGRATE ===")
            try:
                call_command('migrate', '--run-syncdb', '--noinput', verbosity=2)
                print("✅ Syncdb migrate başarılı")
            except Exception as e:
                print(f"⚠️ Syncdb migrate hatası: {str(e)}")
            
            # 4. Final migrate
            print("\n=== 4. FINAL MIGRATE ===")
            try:
                call_command('migrate', '--noinput', verbosity=2)
                print("✅ Final migrate başarılı")
            except Exception as e:
                print(f"⚠️ Final migrate hatası: {str(e)}")
            
            # Restore stdout
            sys.stdout = old_stdout
            
            migration_output = output.getvalue()
            html_output += migration_output
            html_output += "</pre><h3>✅ Migration İşlemi Tamamlandı!</h3>"
            
        except Exception as e:
            sys.stdout = old_stdout
            html_output += f"</pre><h3>❌ Migration Genel Hatası:</h3><p>{str(e)}</p>"
    
    # Database durumu test
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        html_output += f"<h3>📊 Database Tabloları ({len(tables)}):</h3><ul>"
        for table in tables:
            html_output += f"<li>{table}</li>"
        html_output += "</ul>"
        
        # Critical tables check
        critical_tables = ['auth_user', 'anasayfa_dizifilm', 'anasayfa_geziblog']
        html_output += "<h3>🔍 Kritik Tablolar:</h3><ul>"
        for table in critical_tables:
            if table in tables:
                html_output += f"<li style='color: green;'>✅ {table}</li>"
            else:
                html_output += f"<li style='color: red;'>❌ {table} EKSİK</li>"
        html_output += "</ul>"
        
        # User test
        try:
            from django.contrib.auth.models import User
            user_count = User.objects.count()
            superuser_count = User.objects.filter(is_superuser=True).count()
            html_output += f"<h3>👤 Kullanıcılar: {user_count} total, {superuser_count} superuser</h3>"
        except Exception as e:
            html_output += f"<h3>❌ User test hatası: {str(e)}</h3>"
            
    except Exception as e:
        html_output += f"<h3>❌ Database test hatası: {str(e)}</h3>"
    
    # Action buttons
    html_output += f"""
    <h2>🎯 Actions:</h2>
    <div style="margin: 20px 0;">
        <a href="/force-migrate/?run=1" style="background: #dc3545; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">
            🚨 RUN FORCE MIGRATION
        </a>
        <a href="/create-superuser/" style="background: #007bff; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">
            👑 Create Superuser
        </a>
        <a href="/admin/" style="background: #28a745; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">
            🔗 Admin Panel
        </a>
    </div>
    """
    
    html_output += """
    <hr>
    <p><a href="/test/">🧪 Test Page</a> | <a href="/">🏠 Ana Sayfa</a></p>
    """
    
    return HttpResponse(html_output)

def create_superuser_view(request):
    """Manuel superuser oluşturma view'ı - Backup çözüm"""
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    import os
    
    # Default values
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'ramazancan')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ramazan61135@gmail.com')  
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345678Ramazan')
    
    html_output = f"""
    <h1>🔑 Manuel Superuser Oluşturma</h1>
    
    <div style="background: #d1ecf1; color: #0c5460; padding: 20px; border-radius: 10px; border: 1px solid #bee5eb; margin: 20px 0;">
        <h2>🛠️ Manuel Backup Tool</h2>
        <p><strong>Otomatik superuser oluşturma çalışmadıysa bu sayfayı kullanın!</strong></p>
        <p>Bu sayfa güvenli bir şekilde superuser oluşturur veya günceller.</p>
    </div>
    """
    
    # Superuser oluşturma işlemi
    if request.method == 'GET' and 'create' in request.GET:
        html_output += "<h2>🔄 Superuser İşlemi Başlatılıyor...</h2>"
        
        try:
            # Mevcut kullanıcıyı kontrol et
            existing_user = None
            if User.objects.filter(username=username).exists():
                existing_user = User.objects.get(username=username)
                html_output += f"<p>⚠️ Mevcut kullanıcı bulundu: {username}</p>"
                
                # Kullanıcıyı güncelle
                existing_user.set_password(password)
                existing_user.is_superuser = True
                existing_user.is_staff = True
                existing_user.is_active = True
                existing_user.email = email
                existing_user.save()
                
                html_output += f"<p style='color: green;'>✅ Kullanıcı güncellendi: {username}</p>"
            else:
                # Yeni kullanıcı oluştur
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                html_output += f"<p style='color: green;'>🎉 Yeni superuser oluşturuldu: {username}</p>"
            
            # Authentication test
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                html_output += f"<p style='color: green;'>✅ Authentication test başarılı!</p>"
            else:
                html_output += f"<p style='color: red;'>❌ Authentication test başarısız!</p>"
                
        except Exception as e:
            import traceback
            html_output += f"<div style='color: red;'><h3>❌ Superuser oluşturma hatası:</h3><p>{str(e)}</p></div>"
            html_output += f"<pre>{traceback.format_exc()}</pre>"
    
    try:
        # Mevcut kullanıcıları listele
        html_output += "<h2>📊 Mevcut Kullanıcılar:</h2><ul>"
        users = User.objects.all()
        for user in users:
            html_output += f"<li>{user.username} - Staff: {user.is_staff}, Super: {user.is_superuser}, Active: {user.is_active}</li>"
        html_output += f"</ul><p>Toplam: {users.count()} kullanıcı</p>"
        
        # Current superuser info
        html_output += f"<h2>🔑 Hedef Login Bilgileri:</h2>"
        html_output += f"<div style='background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>"
        html_output += f"<p><strong>Username:</strong> {username}</p>"
        html_output += f"<p><strong>Email:</strong> {email}</p>"
        html_output += f"<p><strong>Password:</strong> {password}</p>"
        html_output += f"</div>"
        
        # Authentication test
        html_output += f"<h3>🔐 Şu Anki Authentication Durumu:</h3>"
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            auth_user = authenticate(username=username, password=password)
            
            if auth_user:
                html_output += f"<p style='color: green;'>✅ Authentication başarılı! Admin panele giriş yapabilirsiniz.</p>"
            else:
                html_output += f"<p style='color: orange;'>⚠️ User mevcut ama authentication başarısız. Şifre güncelleme gerekli.</p>"
                
            html_output += f"<p>User bilgileri: Staff={user.is_staff}, Super={user.is_superuser}, Active={user.is_active}</p>"
        else:
            html_output += f"<p style='color: red;'>❌ User henüz yok. Oluşturma gerekli.</p>"
        
    except Exception as e:
        import traceback
        html_output += f"<h3>❌ Database hatası:</h3><p>{str(e)}</p>"
        html_output += f"<pre>{traceback.format_exc()}</pre>"
    
    # Action buttons
    html_output += f"""
    <h2>🎯 Actions:</h2>
    <div style="margin: 20px 0;">
        <a href="/create-superuser/?create=1" style="background: #dc3545; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">
            🔑 CREATE/UPDATE SUPERUSER
        </a>
        <a href="/force-migrate/" style="background: #6c757d; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">
            🚨 Force Migration
        </a>
        <a href="/admin/" style="background: #28a745; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">
            🔗 Admin Panel
        </a>
    </div>
    """
    
    html_output += """
    <hr>
    <p><a href="/test/">🧪 Test Page</a> | <a href="/">🏠 Ana Sayfa</a></p>
    """
    
    return HttpResponse(html_output)

def media_test_view(request):
    """Media files test view'ı"""
    from django.conf import settings
    from .models import DiziFilm, GeziBlog
    import os
    
    html_output = "<h1>📁 Media Files Test</h1>"
    
    # Settings bilgileri
    html_output += f"""
    <h2>⚙️ Media Settings:</h2>
    <ul>
        <li><strong>MEDIA_URL:</strong> {settings.MEDIA_URL}</li>
        <li><strong>MEDIA_ROOT:</strong> {settings.MEDIA_ROOT}</li>
        <li><strong>DEBUG:</strong> {settings.DEBUG}</li>
        <li><strong>RENDER env:</strong> {'RENDER' in os.environ}</li>
    </ul>
    """
    
    # Media dizin kontrolü
    try:
        if os.path.exists(settings.MEDIA_ROOT):
            html_output += f"<h3>✅ Media Root Exists: {settings.MEDIA_ROOT}</h3>"
            
            # Permissions check
            readable = os.access(settings.MEDIA_ROOT, os.R_OK)
            writable = os.access(settings.MEDIA_ROOT, os.W_OK)
            html_output += f"<p>Readable: {readable}, Writable: {writable}</p>"
            
            # List files
            try:
                files = os.listdir(settings.MEDIA_ROOT)
                html_output += f"<h4>Files in MEDIA_ROOT ({len(files)}):</h4><ul>"
                for file in files:
                    file_path = os.path.join(settings.MEDIA_ROOT, file)
                    if os.path.isdir(file_path):
                        # List subdirectory
                        sub_files = os.listdir(file_path)
                        html_output += f"<li><strong>{file}/</strong> ({len(sub_files)} files)<ul>"
                        for sub_file in sub_files[:5]:  # Show max 5 files
                            sub_path = os.path.join(file_path, sub_file)
                            file_size = os.path.getsize(sub_path) if os.path.isfile(sub_path) else 0
                            html_output += f"<li>{sub_file} ({file_size} bytes)</li>"
                        if len(sub_files) > 5:
                            html_output += f"<li>... and {len(sub_files) - 5} more files</li>"
                        html_output += "</ul></li>"
                    else:
                        file_size = os.path.getsize(file_path)
                        html_output += f"<li>{file} ({file_size} bytes)</li>"
                html_output += "</ul>"
            except Exception as e:
                html_output += f"<p>❌ Error listing files: {str(e)}</p>"
        else:
            html_output += f"<h3>❌ Media Root Not Found: {settings.MEDIA_ROOT}</h3>"
    except Exception as e:
        html_output += f"<h3>❌ Error checking Media Root: {str(e)}</h3>"
    
    # Database test
    try:
        dizi_filmler = DiziFilm.objects.all()[:3]
        gezi_bloglari = GeziBlog.objects.all()[:3]
        
        html_output += f"<h2>🎬 DiziFilm Objects ({DiziFilm.objects.count()}):</h2>"
        html_output += f"<h2>🗺️ GeziBlog Objects ({GeziBlog.objects.count()}):</h2>"
        
        for item in dizi_filmler:
            html_output += f"""
            <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
                <h4>📺 {item.isim}</h4>
                <p><strong>Fotoğraf URL:</strong> {item.fotograf.url if item.fotograf else 'No image'}</p>
                {"<p><strong>File exists:</strong> " + str(os.path.exists(item.fotograf.path)) + "</p>" if item.fotograf else "<p>No image file</p>"}
            </div>
            """
            
        for gezi in gezi_bloglari:
            html_output += f"""
            <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
                <h4>🗺️ {gezi.yer_adi}</h4>
                <p><strong>Fotoğraf URL:</strong> {gezi.fotograf.url if gezi.fotograf else 'No image'}</p>
                {"<p><strong>File exists:</strong> " + str(os.path.exists(gezi.fotograf.path)) + "</p>" if gezi.fotograf else "<p>No image file</p>"}
            </div>
            """
            
    except Exception as e:
        html_output += f"<h3>❌ Database Error: {str(e)}</h3>"
    
    html_output += """
    <hr>
    <p><a href="/test/">🧪 Main Test Page</a> | <a href="/gezi-blog-onerileri/">🗺️ Gezi Blog</a> | <a href="/">🏠 Ana Sayfa</a></p>
    """
    
    return HttpResponse(html_output)
