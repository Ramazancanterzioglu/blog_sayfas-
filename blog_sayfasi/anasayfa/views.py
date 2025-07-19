from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import DiziFilm
import os

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

def ornek_sayfa(request):
    return render(request, 'anasayfa/ornek.html')

# Debug için basit test view
def test_view(request):
    import django
    import sys
    from django.db import connection
    from django.contrib.auth.models import User
    
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
                users = User.objects.all()[:3]
                user_list = [f"{u.username} ({'superuser' if u.is_superuser else 'user'})" for u in users]
                user_details = "<br>".join(user_list)
            else:
                user_details = "No users found"
                
        except Exception as e:
            user_status = f"❌ User error: {str(e)}"
            user_details = ""
            
    except Exception as e:
        db_status = f"❌ Database error: {str(e)}"
        tables = []
        user_status = "❌ Can't check users"
        user_details = ""
    
    # DiziFilm test
    try:
        from .models import DiziFilm
        dizi_count = DiziFilm.objects.count()
        dizi_status = f"✅ DiziFilm: {dizi_count} items"
    except Exception as e:
        dizi_status = f"❌ DiziFilm error: {str(e)}"
    
    return HttpResponse(f"""
    <h1>🎉 Django Çalışıyor!</h1>
    <h2>Sistem Bilgileri:</h2>
    <ul>
        <li>Django Version: {django.get_version()}</li>
        <li>Python Version: {sys.version}</li>
        <li>Debug Mode: {settings.DEBUG}</li>
        <li>Allowed Hosts: {settings.ALLOWED_HOSTS}</li>
    </ul>
    
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
