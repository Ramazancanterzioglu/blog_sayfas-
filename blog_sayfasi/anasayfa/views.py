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
    <p><a href="/create-superuser/" style="background: #007cba; color: white; padding: 10px; text-decoration: none;">🔑 Create/Update Superuser</a></p>
    
    <h2>Media Files Test:</h2>
    <p><a href="/media-test/" style="background: #28a745; color: white; padding: 10px; text-decoration: none;">📁 Media Files Debug</a></p>
    
    <h2>Cloudinary Test:</h2>
    <p><a href="/cloudinary-test/" style="background: #17a2b8; color: white; padding: 10px; text-decoration: none;">☁️ Cloudinary Storage Test</a></p>
    
    <h2>Test Linkleri:</h2>
    <ul>
        <li><a href="/">Ana Sayfa</a></li>
        <li><a href="/oran-analizleri/">Oran Analizleri</a></li>
        <li><a href="/muhasebe-terimleri/">Muhasebe Terimleri</a></li>
        <li><a href="/dizi-film-onerileri/">Dizi/Film Önerileri</a></li>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/force-migrate/">🚨 Force Migrate</a></li>
    </ul>
    """)

def force_migrate(request):
    """Acil durum için manuel migration"""
    from django.core.management import call_command
    from io import StringIO
    import sys
    
    output = StringIO()
    
    html_output = "<h1>🚨 Force Migration</h1><h2>Migration Sonuçları:</h2><pre style='background: #f0f0f0; padding: 1rem;'>"
    
    try:
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = output
        
        # Run migrations
        call_command('migrate', '--run-syncdb', verbosity=2)
        call_command('migrate', verbosity=2)
        
        # Restore stdout
        sys.stdout = old_stdout
        
        migration_output = output.getvalue()
        html_output += migration_output
        html_output += "</pre><h3>✅ Migration Tamamlandı!</h3>"
        
        # Test database
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        html_output += f"<h3>Database Tables ({len(tables)}):</h3><ul>"
        for table in tables:
            html_output += f"<li>{table}</li>"
        html_output += "</ul>"
        
        # Test users
        try:
            from django.contrib.auth.models import User
            user_count = User.objects.count()
            html_output += f"<h3>Users: {user_count}</h3>"
        except Exception as e:
            html_output += f"<h3>User test error: {str(e)}</h3>"
            
    except Exception as e:
        sys.stdout = old_stdout
        html_output += f"</pre><h3>❌ Migration Hatası:</h3><p>{str(e)}</p>"
        
    html_output += """
    <hr>
    <p><a href="/test/">Test Page</a> | <a href="/">Ana Sayfa</a> | <a href="/admin/">Admin</a></p>
    """
    
    return HttpResponse(html_output)

def create_superuser_view(request):
    """Manuel superuser oluşturma view'ı"""
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    import os
    
    # Default values
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'ramazancan')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'ramazan61135@gmail.com')  
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345678Ramazan')
    
    html_output = "<h1>🔑 Manuel Superuser Oluşturma</h1>"
    
    try:
        # Mevcut kullanıcıları listele
        html_output += "<h2>📊 Mevcut Kullanıcılar:</h2><ul>"
        users = User.objects.all()
        for user in users:
            html_output += f"<li>{user.username} - Staff: {user.is_staff}, Super: {user.is_superuser}, Active: {user.is_active}</li>"
        html_output += f"</ul><p>Toplam: {users.count()} kullanıcı</p>"
        
        # Superuser oluştur/güncelle
        html_output += f"<h2>🛠️ Superuser İşlemi:</h2>"
        html_output += f"<p>Username: <strong>{username}</strong></p>"
        html_output += f"<p>Email: <strong>{email}</strong></p>"
        html_output += f"<p>Password: <strong>{'*' * len(password)}</strong> ({len(password)} karakter)</p>"
        
        if User.objects.filter(username=username).exists():
            # Mevcut kullanıcıyı güncelle
            user = User.objects.get(username=username)
            
            html_output += f"<h3>🔄 Kullanıcı Güncelleniyor...</h3>"
            html_output += f"<p>Eski bilgiler: Staff={user.is_staff}, Super={user.is_superuser}, Active={user.is_active}</p>"
            
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.email = email
            user.save()
            
            html_output += f"<p>✅ Kullanıcı güncellendi!</p>"
            html_output += f"<p>Yeni bilgiler: Staff={user.is_staff}, Super={user.is_superuser}, Active={user.is_active}</p>"
            
        else:
            # Yeni kullanıcı oluştur
            html_output += f"<h3>🆕 Yeni Kullanıcı Oluşturuluyor...</h3>"
            
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            html_output += f"<p>✅ Yeni superuser oluşturuldu!</p>"
            html_output += f"<p>ID: {user.id}, Staff: {user.is_staff}, Super: {user.is_superuser}</p>"
        
        # Authentication test
        html_output += f"<h3>🔐 Kimlik Doğrulama Testi:</h3>"
        auth_user = authenticate(username=username, password=password)
        
        if auth_user:
            html_output += f"<p>✅ Authentication başarılı!</p>"
            html_output += f"<p>Authenticated user: {auth_user.username}</p>"
            html_output += f"<p>Is authenticated: {auth_user.is_authenticated}</p>"
        else:
            html_output += f"<p>❌ Authentication başarısız!</p>"
            
        # Final superuser list
        html_output += f"<h3>👑 Superuser Listesi:</h3><ul>"
        superusers = User.objects.filter(is_superuser=True)
        for su in superusers:
            html_output += f"<li><strong>{su.username}</strong> ({su.email}) - Active: {su.is_active}</li>"
        html_output += f"</ul><p>Toplam superuser: {superusers.count()}</p>"
        
        # Login link
        html_output += f"""
        <h2>🎯 Admin Panel Giriş:</h2>
        <p><a href="/admin/" target="_blank" style="background: #417690; color: white; padding: 15px; text-decoration: none; font-size: 18px;">
            🔗 Admin Panel'e Git
        </a></p>
        <p><strong>Kullanıcı adı:</strong> {username}</p>
        <p><strong>Şifre:</strong> {password}</p>
        """
        
    except Exception as e:
        import traceback
        html_output += f"<h3>❌ Hata:</h3><p>{str(e)}</p>"
        html_output += f"<pre>{traceback.format_exc()}</pre>"
    
    html_output += """
    <hr>
    <p><a href="/test/">🧪 Test Page</a> | <a href="/">🏠 Ana Sayfa</a></p>
    """
    
    return HttpResponse(html_output)

def media_test_view(request):
    """Media files test view'ı"""
    from django.conf import settings
    from .models import DiziFilm
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
        html_output += f"<h2>🎬 DiziFilm Objects ({DiziFilm.objects.count()}):</h2>"
        
        for item in dizi_filmler:
            html_output += f"""
            <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
                <h4>{item.isim}</h4>
                <p><strong>Fotoğraf field:</strong> {item.fotograf}</p>
                <p><strong>Fotoğraf path:</strong> {item.fotograf.path if item.fotograf else 'No image'}</p>
                <p><strong>Fotoğraf URL:</strong> {item.fotograf.url if item.fotograf else 'No image'}</p>
                
                {"<p><strong>File exists:</strong> " + str(os.path.exists(item.fotograf.path)) + "</p>" if item.fotograf else "<p>No image file</p>"}
                
                {f'<p><strong>File size:</strong> {os.path.getsize(item.fotograf.path)} bytes</p>' if item.fotograf and os.path.exists(item.fotograf.path) else ''}
                
                <p><strong>Full URL Test:</strong> 
                   <a href="{item.fotograf.url if item.fotograf else '#'}" target="_blank">
                       {item.fotograf.url if item.fotograf else 'No URL'}
                   </a>
                </p>
                
                {f'<img src="{item.fotograf.url}" alt="{item.isim}" style="max-width: 200px; max-height: 150px;">' if item.fotograf else '<p>No image to display</p>'}
            </div>
            """
            
    except Exception as e:
        html_output += f"<h3>❌ Database Error: {str(e)}</h3>"
    
    # URL test
    html_output += f"""
    <h2>🔗 URL Tests:</h2>
    <ul>
        <li>Media URL Test: <a href="{settings.MEDIA_URL}" target="_blank">{settings.MEDIA_URL}</a></li>
        <li>Sample image URL: <a href="{settings.MEDIA_URL}dizi_film/interstellar-yildizlararasi-cekildigi-yerler-nerede-cekildi.webp" target="_blank">
            {settings.MEDIA_URL}dizi_film/interstellar-yildizlararasi-cekildigi-yerler-nerede-cekildi.webp</a></li>
    </ul>
    """
    
    html_output += """
    <hr>
    <p><a href="/test/">🧪 Main Test Page</a> | <a href="/dizi-film-onerileri/">🎬 Dizi Film Önerileri</a> | <a href="/">🏠 Ana Sayfa</a></p>
    """
    
    return HttpResponse(html_output)

def cloudinary_test_view(request):
    """Cloudinary bağlantısını test eder"""
    from django.conf import settings
    import os
    
    html_output = "<h1>☁️ Cloudinary Test</h1>"
    
    # Environment variables check
    html_output += f"""
    <h2>🔑 Environment Variables:</h2>
    <ul>
        <li><strong>CLOUDINARY_CLOUD_NAME:</strong> {os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET')}</li>
        <li><strong>CLOUDINARY_API_KEY:</strong> {os.environ.get('CLOUDINARY_API_KEY', 'NOT SET')}</li>
        <li><strong>CLOUDINARY_API_SECRET:</strong> {'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET'}</li>
        <li><strong>RENDER env:</strong> {'RENDER' in os.environ}</li>
    </ul>
    """
    
    # Settings check
    try:
        cloudinary_available = hasattr(settings, 'CLOUDINARY_STORAGE')
        html_output += f"<h3>📋 Settings:</h3>"
        html_output += f"<p>CLOUDINARY_AVAILABLE: {getattr(settings, 'CLOUDINARY_AVAILABLE', False)}</p>"
        html_output += f"<p>DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}</p>"
        
        if cloudinary_available:
            cloudinary_config = getattr(settings, 'CLOUDINARY_STORAGE', {})
            html_output += f"<p>Cloud Name: {cloudinary_config.get('CLOUD_NAME', 'Not set')}</p>"
            html_output += f"<p>API Key: {cloudinary_config.get('API_KEY', 'Not set')}</p>"
            html_output += f"<p>Secure: {cloudinary_config.get('SECURE', False)}</p>"
    except Exception as e:
        html_output += f"<p>❌ Settings error: {str(e)}</p>"
    
    # Cloudinary connection test
    try:
        import cloudinary
        import cloudinary.api
        
        # Test API connection
        html_output += f"<h3>🌐 Connection Test:</h3>"
        
        # Get account info
        try:
            result = cloudinary.api.ping()
            html_output += f"<p>✅ Cloudinary Ping: {result}</p>"
            
            # Get usage info
            usage = cloudinary.api.usage()
            html_output += f"<p>📊 Storage used: {usage.get('credits', {}).get('usage', 0)} / {usage.get('credits', {}).get('limit', 0)}</p>"
            html_output += f"<p>📊 Bandwidth used: {usage.get('bandwidth', {}).get('usage', 0)} / {usage.get('bandwidth', {}).get('limit', 0)}</p>"
            
        except Exception as api_e:
            html_output += f"<p>❌ API connection failed: {str(api_e)}</p>"
            html_output += f"<p>💡 Bu normal - Cloudinary ayarları henüz yapılmamış olabilir</p>"
            
    except ImportError:
        html_output += f"<p>❌ Cloudinary paketleri yüklenmemiş</p>"
    except Exception as e:
        html_output += f"<p>❌ Cloudinary test error: {str(e)}</p>"
    
    # Instructions
    html_output += f"""
    <h2>🚀 Cloudinary Kurulum Adımları:</h2>
    <ol>
        <li><strong>Cloudinary hesabı açın:</strong> <a href="https://cloudinary.com" target="_blank">cloudinary.com</a></li>
        <li><strong>Dashboard'dan şu bilgileri alın:</strong>
            <ul>
                <li>Cloud Name</li>
                <li>API Key</li>
                <li>API Secret</li>
            </ul>
        </li>
        <li><strong>Render Environment Variables'a ekleyin:</strong>
            <ul>
                <li>CLOUDINARY_CLOUD_NAME</li>
                <li>CLOUDINARY_API_KEY</li>
                <li>CLOUDINARY_API_SECRET</li>
            </ul>
        </li>
        <li><strong>Deploy edin</strong></li>
    </ol>
    """
    
    html_output += """
    <hr>
    <p><a href="/test/">🧪 Main Test</a> | <a href="/media-test/">📁 Media Test</a> | <a href="/">🏠 Ana Sayfa</a></p>
    """
    
    return HttpResponse(html_output)
