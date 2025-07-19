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
        if settings.DEBUG:
            return HttpResponse(f"""
            <h1>Dizi/Film Önerileri Sayfası Hatası</h1>
            <p><strong>Hata:</strong> {str(e)}</p>
            <p><strong>Hata Türü:</strong> {type(e).__name__}</p>
            <hr>
            <p><a href="/">Ana Sayfaya Dön</a></p>
            """)
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
    return HttpResponse(f"""
    <h1>🎉 Django Çalışıyor!</h1>
    <h2>Sistem Bilgileri:</h2>
    <ul>
        <li>Django Version: {django.get_version()}</li>
        <li>Python Version: {sys.version}</li>
        <li>Debug Mode: {settings.DEBUG}</li>
        <li>Allowed Hosts: {settings.ALLOWED_HOSTS}</li>
    </ul>
    <h2>Test Linkleri:</h2>
    <ul>
        <li><a href="/">Ana Sayfa</a></li>
        <li><a href="/oran-analizleri/">Oran Analizleri</a></li>
        <li><a href="/muhasebe-terimleri/">Muhasebe Terimleri</a></li>
        <li><a href="/dizi-film-onerileri/">Dizi/Film Önerileri</a></li>
    </ul>
    """)
