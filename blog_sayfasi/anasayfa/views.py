from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
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
    </ul>
    """)
