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

def dizi_film_detay(request, pk):
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
